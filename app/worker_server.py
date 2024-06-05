from fastapi import FastAPI
import time
import random
import requests

app = FastAPI()


@app.get("/start/")
async def start_order():
    resp = requests.post(
        "http://127.0.0.1:8000/order?client_id=worker&worker_flag=fetch"
    )
    order_array = resp.json()
    for order in order_array:
        order["status"] == "pending"
        requests.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=start"
        )
        time.sleep(random.randint(30, 60))
        requests.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=brewed"
        )
        return f"finished brewing for {order['client_id']}"
    return "No available orders"


@app.post("/finish/")
async def finish_order(client_id: str):
    resp = requests.post(
        "http://127.0.0.1:8000/order?client_id=worker&worker_flag=fetch"
    )
    order_array = resp.json()
    for order in order_array:
        if order["client_id"] == client_id:
            requests.post(
                f"http://127.0.0.1:8000/order?client_id={client_id}&worker_flag=finish"
            )
            return f"deleveried {client_id} order"
    return f"No orders for the client - {client_id}"
