from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import datetime
import json
import os

app = FastAPI()

# Replace these with your real wallet addresses
BTC_WALLET = "bc1qh8es4m9mjua5w08qv00"
USDT_WALLET = "TE6bcewMeHxn8USQ65baJh4ynx8Qw5dvop"

@app.get("/")
def root():
    return {
        "message": "LGBTQ+ Justice Donation API is live.",
        "donate_btc": BTC_WALLET,
        "donate_usdt_trc20": USDT_WALLET
    }

@app.post("/donate")
async def receive_donation(
    name: str = Form(...),
    amount: float = Form(...),
    currency: str = Form(...),
    method: str = Form(...)
):
    donation = {
        "name": name,
        "amount": amount,
        "currency": currency,
        "method": method,
        "timestamp": str(datetime.datetime.utcnow())
    }

    if not os.path.exists("donations.json"):
        with open("donations.json", "w") as f:
            json.dump([], f)

    with open("donations.json", "r+") as f:
        data = json.load(f)
        data.append(donation)
        f.seek(0)
        json.dump(data, f, indent=4)

    return {"message": "Donation received successfully!"}
