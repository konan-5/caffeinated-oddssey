from fastapi import FastAPI
import aiohttp
import asyncio
import random

app = FastAPI()


async def process_order(order):
    async with aiohttp.ClientSession() as session:
        await session.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=start"
        )
        await asyncio.sleep(random.randint(30, 60))
        await session.post(
            f"http://127.0.0.1:8000/order?client_id={order['client_id']}&worker_flag=brewed"
        )
        return f"finished brewing for {order['client_id']}"


@app.get("/start/")
async def start_order():
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
            return f"delivered {client_id} order"
    return f"No orders for the client - {client_id}"
