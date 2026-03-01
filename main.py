import json
import logging
import httpx
from datetime import datetime
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

ZAPIER_URL = "https://hooks.zapier.com/hooks/catch/26586869/u0sxxf5/"

@app.post("/send-to-zapier")
async def send_to_zapier():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    payload = {
        "Email": f"{timestamp}@Test.com",
        "Id": timestamp,
        "IsActive": "TRUE",
        "Name": f"Test_{timestamp}"
    }
    logger.info("Sending payload to Zapier:\n%s", json.dumps(payload, indent=2))
    async with httpx.AsyncClient() as client:
        response = await client.post(ZAPIER_URL, json=payload)
    logger.info("Zapier response [%s]: %s", response.status_code, response.text)
    return {
        "sent_payload": payload,
        "zapier_status": response.status_code,
        "zapier_response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
    }
