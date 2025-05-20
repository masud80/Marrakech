FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./serving ./serving
COPY ./models ./models
COPY ./pipelines ./pipelines

CMD ["uvicorn", "serving.main:app", "--host", "0.0.0.0", "--port", "8500", "--reload"] 