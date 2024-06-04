# The Caffeinated Odyssey

## Overview

This project involves setting up two FastAPI servers: one for clients to place coffee orders and another for baristas to process these orders, using a shared in-memory queue to manage the order flow. The client server handles incoming orders and adds them to the queue, while the worker server retrieves and processes orders, ensuring a smooth and efficient coffee-making workflow.

## Setup and Execution

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/caffeinated_odyssey.git
    cd caffeinated_odyssey
    ```

2. **Build and Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3. **Access the Services**:
    - Client orders: `http://localhost/order/`
    - Worker start: `http://localhost/start/`
    - Worker finish: `http://localhost/finish/`

## Anti-DDoS Measures

The nginx configuration in `nginx/default.conf` includes rate limiting to protect against DDoS attacks.
