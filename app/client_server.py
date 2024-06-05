import time
import asyncio
from typing import List, Dict, Tuple
from fastapi import FastAPI, Request, Query, HTTPException
from models import Order

# Create an instance of FastAPI
app = FastAPI(
    title="Order API",
    description="This is a simple API to order a new caffeine.",
    version="1.0.0",
)

# Array to store orders
order_array: List[Order] = []
# Dictionary to keep track of order counts and timestamps per IP
order_counts: Dict[str, Tuple[int, List[float]]] = {}
BLOCK_THRESHOLD = 1000  # Maximum number of orders allowed from one IP
BLOCK_TIMEFRAME = 60 * 60  # Timeframe in seconds (1 hour)


@app.post("/order/")
async def place_order(
    request: Request,
    client_id: str,
    worker_flag: str = Query("", include_in_schema=False),
):
    """
    Place a new order.
    """
    client_ip = request.client.host
    current_time = time.time()

    # Initialize or update order counts for the client IP
    if client_ip not in order_counts:
        order_counts[client_ip] = (0, [])

    order_count, timestamps = order_counts[client_ip]

    # Clean up old timestamps
    order_counts[client_ip] = (
        order_count,
        [ts for ts in timestamps if current_time - ts <= BLOCK_TIMEFRAME],
    )

    # Check if the client IP has exceeded the maximum allowed orders
    if len(order_counts[client_ip][1]) >= BLOCK_THRESHOLD:
        raise HTTPException(
            status_code=403,
            detail="You have exceeded the maximum number of allowed orders.",
        )

    # Handle different worker flags for order management
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
            if order_array[order_idx].status:
                return "already delivered"
            order_array[order_idx].status = "delivered"
            return "delivered"

    if worker_flag == "fetch":
        return order_array

    # Create a new order and add it to the array
    order = Order(client_id=client_id, status="pending")
    order_array.append(order)
    order.id = len(order_array)

    # Update order count and timestamps for the client IP
    order_counts[client_ip][1].append(current_time)

    # Wait until the order is delivered
    while True:
        if order.status == "delivered":
            return "success"
        await asyncio.sleep(1)
