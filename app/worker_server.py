from fastapi import FastAPI
import aiohttp
import asyncio
import random

# Create an instance of FastAPI
app = FastAPI(
    title="Baristas API",
    description="This API manages the processing of orders, including starting and finishing the order processing.",
    version="1.0.0",
)


async def process_order(order):
    """
    Simulate the processing of an order.
    """
    async with aiohttp.ClientSession() as session:
        # Notify that the order processing has started
        await session.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=start"
        )
        print("brewing started")
        # Simulate brewing time
        await asyncio.sleep(random.randint(30, 60))
        # Notify that the order has been brewed
        await session.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=brewed"
        )
        return f"Finished brewing for {order['client_id']}"


@app.get("/start/")
async def start_order():
    """
    Start processing orders that are waiting.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/order?client_id=worker&worker_flag=fetch"
        ) as resp:
            order_array = await resp.json()

    tasks = []
    for order in order_array:
        if order["status"] == "pending":
            tasks.append(process_order(order))

    if tasks:
        results = await asyncio.gather(*tasks)
        return results
    else:
        return "No available orders"


@app.post("/finish/")
async def finish_order(client_id: str):
    """
    Finish processing a specific order by client ID.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8000/order?client_id=worker&worker_flag=fetch"
        ) as resp:
            order_array = await resp.json()

    for order in order_array:
        if order["client_id"] == client_id:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    f"http://127.0.0.1:8000/order?client_id={client_id}&worker_flag=finish"
                )
            return f"Delivered {client_id} order"
    return f"No orders for the client - {client_id}"
