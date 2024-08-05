from bs4 import BeautifulSoup
import json
import time
import requests
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from auth import get_token_header
from cache_keys import PRODUCT_DETAILS_CACHE_KEY
from config import API_TIMEOUT, DEFAULT_HEADERS, SCRAPPING_BASE_URL
from notifier import ConsoleNotifier
from storage_strategy import Storage

router = APIRouter()


def get_website_data(endpoint_url: str, headers: dict, timeout: int = API_TIMEOUT,
                     proxy: dict = None, retries: int = 3, retry_interval: int = 5):
    while retries > 0:
        try:
            response = requests.get(
                endpoint_url,
                headers=headers,
                timeout=timeout,
                proxies=proxy
            )
            response.raise_for_status()
            return response.content
        except requests.HTTPError as e:
            print(f"Error while fetching data from {endpoint_url}", e)
            retries -= 1
            time.sleep(retry_interval)


@router.get("/scrap", dependencies=[Depends(get_token_header)])
def scrap(pages: int = Query(default=5), proxy: str = Query(default=None)):
    try:
        headers = json.loads(DEFAULT_HEADERS)
        proxy = {"http": proxy, "https": proxy} if proxy else None
        products_scrapped = 0
        for page in range(1, pages + 1):
            scraped_data = []
            api_endpoint = f"{SCRAPPING_BASE_URL}page/{page}/"
            data = get_website_data(api_endpoint, headers, proxy=proxy)
            if not data:
                continue
            soup = BeautifulSoup(data, "html.parser")
            products = soup.select(".products .product")

            for product in products:
                title = product.select_one(".woo-loop-product__title").text.strip().strip(".")
                price = product.select_one(".price .amount").text.strip()[1:]

                products_cache_key = PRODUCT_DETAILS_CACHE_KEY.format(product_title=title)

                # Check if the product is already scrapped and its price is same
                redis_storage = Storage.get_storage_technique("redis")
                redis_storage = redis_storage(products_cache_key)
                redis_data = redis_storage.get_data()
                if redis_data and redis_data["product_price"] == price:
                    # Skip the product if it is already scrapped and price is same
                    continue
                
                image_url = product.select_one(".mf-product-thumbnail img")["data-lazy-src"]
                image_response = requests.get(image_url, timeout=API_TIMEOUT)
                image_path = f"{title.replace(' ', '_')}.jpg"
                img_local_storage = Storage.get_storage_technique("local")
                path_to_image = img_local_storage(image_path).save_image(image_response.content)

                # Save the product details to cache
                redis_storage.save_data({
                    "product_title": title,
                    "product_price": price,
                    "path_to_image": path_to_image,
                })
                scraped_data.append({
                    "product_title": title,
                    "product_price": price,
                    "path_to_image": path_to_image,
                })
                products_scrapped += 1
            file_storage = Storage.get_storage_technique("local")
            file_storage("products.json").save_data(scraped_data)

        message = f"Total Products Scrapped : {products_scrapped}"
        ConsoleNotifier().notify(message)

        return {
            "scrapping": "done",
            "total_products_scrapped": products_scrapped
        }
    except Exception:
        return JSONResponse({"error": "Error while scrapping the data"},
                            status_code=500)
