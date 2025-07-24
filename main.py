from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import datetime

app = FastAPI()

BTC_WALLET = "bc1qh8es4m9mjua5w08qv00"
USDT_WALLET = "TE6bcewMeHxn8USQ65baJh4ynx8Qw5dvop"

@app.get("/")
def read_root():
    return {
        "message": "LGBTQ+ donation backend is running.",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/donate")
async def donate(request: Request):
    data = await request.json()
    print("Donation received:", data)
    return {"status": "success", "data": data}
