import time
from typing import List
from fastapi import FastAPI, Request, Query
from models import Order

app = FastAPI()

order_array: List[Order] = []


@app.get("/")
def fetch_order():
    return order_array


@app.post("/order/")
def place_order(
    request: Request,
    client_id: str,
    worker_flag: str = Query("", include_in_schema=False),
):
    if worker_flag == "fetch":
        return order_array

    if worker_flag == "start" or worker_flag == "finish" or worker_flag == "brewed":
        if not order_array:
            return "No available orders"

        order_idx = None
        for idx, order in enumerate(order_array):
            if order.client_id == client_id:
                order_idx = idx
                break

        if order_idx is None:
            return "No orders with that client_id"

        if worker_flag == "start":
            order_array[order_idx].status = "brewing"
            return "brewing"
        elif worker_flag == "brewed":
            order_array[order_idx].status = "brewed"
            return "brewed"
        elif worker_flag == "finish":
            order_array[order_idx].status = "delivered"
            return "delivered"

    else:
        order = Order(client_id=client_id, status="pending")

        order_array.append(order)
        order.id = len(order_array)

        while True:
            if order.status == "delivered":
                return "success"
            time.sleep(1)
