from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
import datetime
import requests
import json

app = FastAPI()

# ✅ Your real Flutterwave keys
FLUTTERWAVE_PUBLIC_KEY = "FLWPUBK_TEST-01069d9356ac10c70d00703d4ff1e8f3-X"
FLUTTERWAVE_SECRET_KEY = "FLWSECK_TEST-f2e4577b39c4a086c041a00a9535e3db-X"

# ✅ Your real wallet addresses
WALLETS = {
    "BTC": "bc1qh8es4m9mjua5w08qv00",
    "USDT": "UQCtCm584SIWPddaOQ9ec8MULk2Aqi5ucw2s073DzNtQQc6L",
    "ETH": "0xf22566f4a5b70437e33f8c846e3780f4609e2abe",
    "XRP": "rf9nJMNU3Y2D8EkeDG4Z4f9qUPhThdrsGk",
    "SOL": "5msvCNwA3boDLKrgBEA8MPTnFq4bfeEqTttyEnr2nnsM",
    "BCH": "bitcoincash:qzk5keejgnc0urhqtrq3lk8xrus6nef5gvxh4476qa"
}

LOG_FILE = "payment_logs.txt"

def log_payment(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

@app.get("/", response_class=HTMLResponse)
async def homepage():
    crypto_list = "".join([f"<option value='{coin}'>{coin}</option>" for coin in WALLETS])
    return f"""
    <html>
        <head><title>CryptoPay Genius</title></head>
        <body style='font-family:sans-serif;padding:20px;max-width:500px;margin:auto'>
            <h2>CryptoPay Genius</h2>
            <form action="/pay" method="post">
                <label>Amount:</label><br/>
                <input type="number" name="amount" required><br/><br/>

                <label>Currency:</label><br/>
                <select name="currency" required>
                    <option value="USD">USD</option>
                    <option value="NGN">NGN</option>
                    <option value="EUR">EUR</option>
                    <option value="GBP">GBP</option>
                    <option value="KES">KES</option>
                </select><br/><br/>

                <button type="submit">Pay with Card</button>
            </form>

            <hr/>

            <h3>Or Pay with Crypto</h3>
            <form action="/crypto" method="post">
                <label>Choose Coin:</label><br/>
                <select name="coin" required>
                    {crypto_list}
                </select><br/><br/>
                <label>Amount (USD equivalent):</label><br/>
                <input type="number" name="amount" required><br/><br/>
                <button type="submit">Show Wallet</button>
            </form>
        </body>
    </html>
    """

@app.post("/pay")
async def pay_with_flutterwave(amount: float = Form(...), currency: str = Form(...)):
    tx_ref = str(uuid.uuid4())
    payload = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": currency,
        "redirect_url": "https://pay-2-2.onrender.com/thankyou",
        "payment_options": "card,ussd,banktransfer",
        "customer": {
            "email": f"user{uuid.uuid4().hex[:5]}@genius.com",
            "name": "CryptoPay User"
        },
        "customizations": {
            "title": "CryptoPay Genius",
            "description": f"Payment of {amount} {currency}"
        }
    }

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
    result = response.json()
    
    if result.get("status") == "success":
        payment_link = result["data"]["link"]
        log_payment({"method": "card", "amount": amount, "currency": currency, "tx_ref": tx_ref, "timestamp": str(datetime.datetime.now())})
        return HTMLResponse(f'<a href="{payment_link}">Click to Pay</a>')
    else:
        return {"error": result.get("message", "Something went wrong.")}

@app.post("/crypto", response_class=HTMLResponse)
async def crypto_payment(coin: str = Form(...), amount: float = Form(...)):
    wallet = WALLETS.get(coin)
    if not wallet:
        return "Invalid coin selected."

    log_payment({"method": "crypto", "coin": coin, "wallet": wallet, "amount": amount, "timestamp": str(datetime.datetime.now())})

    return f"""
    <html>
        <body style='font-family:sans-serif;padding:20px;'>
            <h3>Send {amount} USD worth of {coin} to:</h3>
            <p style='font-size:18px;font-weight:bold'>{wallet}</p>
            <p>After sending, we'll confirm manually.</p>
        </body>
    </html>
    """

@app.get("/thankyou", response_class=HTMLResponse)
async def thank_you():
    return "<h2>Thank you for your payment!</h2>"
