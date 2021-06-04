FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
