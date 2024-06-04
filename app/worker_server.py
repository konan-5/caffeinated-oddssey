from fastapi import FastAPI, BackgroundTasks
from .models import Order
from .shared_data import orders_queue
from time import sleep
import random

app_worker = FastAPI()

@app_worker.get("/start/")
async def start_order():
    if not orders_queue.empty():
        order_dict = orders_queue.get()
        order = Order(**order_dict)  # Deserialize the dictionary to an Order object
        return order
    return {"message": "No orders"}

@app_worker.post("/finish/")
async def finish_order(order: Order, background_tasks: BackgroundTasks):
    def process_order():
        sleep(random.randint(30, 60))  # Simulate brewing time
        print(f"Order for client {order.client_id} is ready")

    background_tasks.add_task(process_order)
    return {"message": "Order is being processed"}
