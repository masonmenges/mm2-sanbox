FROM prefecthq/prefect:2.16.2-python3.11-kubernetes
COPY requirements.txt .
RUN pip install -r requirements.txt