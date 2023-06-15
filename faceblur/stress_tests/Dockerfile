FROM python:3.8

WORKDIR /locust

RUN pip install locust

COPY . .

CMD ["locust", "-f", "locustfile.py"]