import base64
from flask import Flask, request
import json
import os
import mysql.connector
app = Flask(__name__)


@app.post("/loadcustomers", strict_slashes=False)
def message_received():    
    envelope = request.get_json()
    print(f"envelope: {envelope}")
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        payload = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        payload_json = json.loads(payload)
        for customer in payload_json:
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
