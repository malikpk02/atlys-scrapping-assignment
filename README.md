# Web Scraping Tool with FastAPI

This project is a web scraping tool built using FastAPI. It scrapes product information from a given website and stores the data in various storage backends. Additionally, it supports a retry mechanism for failed requests, caching to avoid redundant updates, and a notification system to report the scraping status.

## Features

- Scrap product name, price, and image from multiple pages of a catalog.
- Optional settings to limit the number of pages to scrap and to use a proxy.
- Storage of scraped data in different backends (local storage, Redis).
- Caching mechanism using Redis to avoid redundant updates.
- Retry mechanism for handling server errors.
- Notification system to report the scraping status.

## Requirements

- Python 3.8+
- Redis server

## Installation

1. Clone the repository:

    ```bash
    https://github.com/malikpk02/atlys-scrapping-assignment.git
    cd atlys-scrapping-assignment
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip3 install -r requirement.txt
    ```

4. Ensure Redis is installed and running on your system:

    - For Ubuntu:

        ```bash
        sudo apt-get install redis-server
        sudo service redis-server start
        ```

    - For macOS:

        ```bash
        brew install redis
        brew services start redis
        ```
5. Create a `.env` file and initialize environment variables. Example:
   ```
   SCRAPPING_BASE_URL="{your-scrapping-webiste}"
   DEFAULT_HEADERS={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
   API_TIMEOUT="{api-timeout}"
   STATIC_TOKEN = "{your-static-token}"
   REDIS_HOST="{redis-host}"
   REDIS_PORT="{redis-port}"
   ```

## Usage

1. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

2. Access the scraping endpoint in your browser or using a tool like `curl` or Postman:

    ```bash
    http://127.0.0.1:8000/api/v1/scrap?pages=5
    ```

    - `pages`: Number of pages to scrap.
    - `proxy`: Proxy to use for scrapping api

## Configuration

### Storage

- **Local Storage**: Data is stored in a JSON file on your local system.
- **Redis Storage**: Data is stored in an Redis.
### Notifier

- **Console Notifier**: Prints the scraping status to the console. Extend this by implementing the `Notifier` interface in `notifier.py` to add other notification strategies.

## Code Structure

- `main.py`: Main FastAPI application file containing the scraper logic.
- `storage_strategy.py`: Contains storage strategy classes for local storage and Redis storage.
- `cache.py`: Contains the Redis caching logic.
- `notifier.py`: Contains the notifier interface and console notifier implementation.
- `auth.py`: Handles user authentication using static tokens for secure access to FastAPI endpoints.
- `config.py`: Manages configuration settings by loading environment variables from a .env file.


## Extending the Project

1. **Adding New Storage Backends**: Implement the `Storage` strategy interface for the new storage backend and update the `get_storage` function.
2. **Adding New Notifiers**: Implement the `Notifier` interface and create a new notifier class. Update the `notify` function to use the new notifier.
3. **Customizing Retry Logic**: Adjust the `retries` and `retry_interval` in `main.py` to change the retry behavior.


