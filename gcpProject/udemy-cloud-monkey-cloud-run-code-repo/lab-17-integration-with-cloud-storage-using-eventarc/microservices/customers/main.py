import base64
from flask import Flask, request
from cloudevents.http import from_http
from google.cloud import storage
import json
import os
import mysql.connector
app = Flask(__name__)


@app.post("/loadcustomers", strict_slashes=False)
def message_received():    
    event = from_http(request.headers, request.get_data())
    print(f"event:{event}")
    data = event.data

    bucket_name = data["bucket"]
    object_name = data["name"]

    
    # gcs_object = os.path.join(bucket_name, object_name)

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(object_name)

    blob.download_to_filename(object_name)

    with open(object_name) as f:
        file_data = json.load(f)
        print(file_data)
    
    for customer in file_data:
        print(f"Customer to load: {customer} ")
        insert_customer(customer)

    return "", 204

def insert_customer(customer):
    DB_UNIX_SOCKET_DIR="/cloudsql"
    CLOUD_SQL_CONNECTION_NAME=os.getenv("CLOUD_SQL_CONNECTION_NAME")
    DB_USER=os.getenv("DB_USER","root")
    DB_PASSWORD=os.getenv("DB_PASSWORD","passw0rd")

    query = f"INSERT INTO customers VALUES {customer['customer_id'], customer['name'], customer['address'], customer['city'], customer['state'], customer['zipcode'], customer['country'], customer['entry_type']}"
    print(query)
    
    with mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, unix_socket=f"{DB_UNIX_SOCKET_DIR}/{CLOUD_SQL_CONNECTION_NAME}", database='customer_mgmt') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
