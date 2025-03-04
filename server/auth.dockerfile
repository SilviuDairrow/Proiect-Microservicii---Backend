FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

COPY . /app

RUN pip install grpcio grpcio-tools psycopg2 bcrypt PyJWT cryptography

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. auth.proto

EXPOSE 50051

CMD ["python", "auth_server.py"]