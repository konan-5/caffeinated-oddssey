# Caffeinated Odyssey

Caffeinated Odyssey is a FastAPI-based project that simulates a coffee ordering system. It includes two main services: a client server for placing and managing orders and a worker server for processing these orders.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/caffeinated-odyssey.git
cd caffeinated-odyssey
```

2. Build and start the Docker containers using Docker Compose:

```sh
docker-compose up --build
```

This will build the Docker images and start the `client_server` on port 8000 and `worker_server` on port 8001.

### Usage

The client server exposes the following endpoints:

- **POST /order/**: Place an order with a client ID.

The worker server exposes the following endpoints:

- **GET /start/**: Fetch pending orders and start brewing.
- **POST /finish/**: Mark an order as delivered by providing the `client_id`.

### API Endpoints

#### Client Server

- **POST /order/**:
  - Description: Place a new order or update an existing order status.
  - Parameters:
    - `client_id` (query): The ID of the client.
  - Response: Order status.

#### Worker Server

- **GET /start/**:
  - Description: Fetch pending orders and start brewing.
  - Response: Brewing status or message if no orders are available.

- **POST /finish/**:
  - Description: Mark an order as delivered.
  - Parameters:
    - `client_id` (query): The ID of the client.
  - Response: Delivery status or message if no orders are found for the client.

### Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container Docker applications

### Contributing

Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are accepted.

### Authors

- **Ikeda Hiroshi** - [konan-5](https://github.com/konan-5)
