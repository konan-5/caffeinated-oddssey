from fastapi import FastAPI, Request, HTTPException, status
from .models import Order
from .shared_data import orders_queue

app_client = FastAPI()
blocked_ips = set()
MAX_REQUESTS = 1000

@app_client.post("/order/")
async def place_order(request: Request, order: Order):
    client_ip = request.client.host

    if client_ip in blocked_ips:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    if orders_queue.qsize() >= MAX_REQUESTS:
        blocked_ips.add(client_ip)
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests")

    orders_queue.put(order)
    return {"message": "Order received"}

@app_client.get("/orders/")
async def get_orders():
    return {"orders": list(orders_queue.queue)}
