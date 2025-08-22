from fastapi import FastAPI
import logging
import uvicorn

from src.api.middleware import RateLimitMiddleware
from src.api.routes import router as api_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Cashflower API")


@app.get("/")
def read_root():
    return {"message": "Cashflower API is running!"}


@app.get("/ping")
def ping():
    return {"message": "pong"}


app.add_middleware(RateLimitMiddleware)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
