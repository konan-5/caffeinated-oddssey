FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app
COPY ./app /app

# Copy Nginx configuration files
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
