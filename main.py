from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import datetime
import json
import os

app = FastAPI()

# Load from environment variables
BTC_WALLET = os.getenv("BTC_WALLET")
USDT_WALLET = os.getenv("USDT_WALLET")
ETH_WALLET = os.getenv("ETH_WALLET")
XRP_WALLET = os.getenv("XRP_WALLET")
SOL_WALLET = os.getenv("SOL_WALLET")
FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")
THANK_YOU_URL = os.getenv("THANK_YOU_URL", "https://thankyou.page")  # default if not set

# Log function
def log_donation(data):
    with open("donations_log.json", "a") as f:
        f.write(json.dumps(data) + "\n")

# Flutterwave webhook
class FlutterwaveWebhook(BaseModel):
    data: dict

@app.post("/webhook/flutterwave")
async def flutterwave_webhook(payload: FlutterwaveWebhook):
    data = payload.data
    if data.get("status") == "successful":
        log_donation({
            "type": "flutterwave",
            "amount": data.get("amount"),
            "currency": data.get("currency"),
            "email": data.get("customer", {}).get("email"),
            "name": data.get("customer", {}).get("name"),
            "timestamp": str(datetime.datetime.now())
        })
    return {"status": "ok"}

# Crypto form handler
@app.post("/donate-crypto")
async def donate_crypto(
    method: str = Form(...),
    amount: str = Form(...),
    sender: str = Form(...)
):
    log_donation({
        "type": "crypto",
        "method": method,
        "amount": amount,
        "sender": sender,
        "timestamp": str(datetime.datetime.now())
    })
    return RedirectResponse(url=THANK_YOU_URL, status_code=303)

# Show wallets if needed (GET request)
@app.get("/wallets")
async def get_wallets():
    return {
        "BTC": BTC_WALLET,
        "USDT": USDT_WALLET,
        "ETH": ETH_WALLET,
        "XRP": XRP_WALLET,
        "SOL": SOL_WALLET
}
