FROM prefecthq/prefect:2.14.20-python3.11-kubernetes
COPY requirements.txt .
RUN pip install -r requirements.txt