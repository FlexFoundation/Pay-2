from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import datetime
import json
import uvicorn
import os

app = FastAPI()

# Use the templates folder
templates = Jinja2Templates(directory="templates")

# Your Flutterwave public key and encryption key from Render environment
FLW_PUBLIC_KEY = os.getenv("FLW_PUBLIC_KEY")
FLW_ENCRYPTION_KEY = os.getenv("FLW_ENCRYPTION_KEY")

@app.get("/", response_class=HTMLResponse)
async def payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})

@app.post("/process-payment")
async def process_payment(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    amount: float = Form(...)
):
    # Prepare a mock payload for Flutterwave (replace later with actual integration)
    payment_data = {
        "status": "pending",
        "payer_name": name,
        "payer_email": email,
        "amount": amount,
        "currency": "USD",
        "date": datetime.datetime.now().isoformat()
    }

    # Log to JSON file (optional)
    with open("payments.json", "a") as f:
        f.write(json.dumps(payment_data) + "\n")

    return RedirectResponse(url="/", status_code=303)
