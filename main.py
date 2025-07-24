from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

FLW_PUBLIC_KEY = os.getenv("FLW_PUBLIC_KEY")
FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")
FLW_ENCRYPTION_KEY = os.getenv("FLW_ENCRYPTION_KEY")

class PaymentData(BaseModel):
    name: str
    email: str
    amount: float

@app.get("/", response_class=HTMLResponse)
async def payment_form(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@app.post("/process-payment")
async def process_payment(request: Request, name: str = Form(...), email: str = Form(...), amount: float = Form(...)):
    payload = {
        "tx_ref": f"tx-{os.urandom(6).hex()}",
        "amount": amount,
        "currency": "USD",
        "redirect_url": "https://google.com",  # change this to your thank-you or success page
        "payment_options": "card",
        "customer": {
            "email": email,
            "name": name
        },
        "customizations": {
            "title": "Support Payment",
            "description": "Thank you for your support!"
        }
    }

    headers = {
        "Authorization": f"Bearer {FLW_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers=headers)
    res_data = response.json()

    if res_data.get("status") == "success":
        return RedirectResponse(url=res_data["data"]["link"])
    else:
        return {"error": "Failed to initiate payment"}
