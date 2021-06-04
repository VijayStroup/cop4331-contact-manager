FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
