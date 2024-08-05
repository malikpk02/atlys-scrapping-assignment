from fastapi import FastAPI
from routers.scrapping import router as scrapping_router

app = FastAPI()
app.include_router(scrapping_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World"}
