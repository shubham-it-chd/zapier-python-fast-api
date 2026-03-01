import json
import logging
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def main():
    return {"message": "Hello World"}

@app.post("/echo")
async def echo(request: Request):
    payload = await request.json()
    logger.info("Received payload:\n%s", json.dumps(payload, indent=2))
    return payload
