from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

MICROSERVICES = {
    "auth": "http://auth_service:8000",
    "transactions": "http://transactions_service:8000",
    "shop": "http://shop_service:8000",
    "notifications": "http://notifications_service:8000",
}

@app.post("/register/")
async def register_user(user_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MICROSERVICES['auth']}/register/", json=user_data)
        return response.json()

@app.post("/login/")
async def login_user(credentials: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MICROSERVICES['auth']}/login/", json=credentials)
        return response.json()

@app.post("/transactions/")
async def create_transaction(transaction_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MICROSERVICES['transactions']}/transactions/", json=transaction_data)
        return response.json()

@app.get("/shop/items/")
async def get_items():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MICROSERVICES['shop']}/items/")
        return response.json()
