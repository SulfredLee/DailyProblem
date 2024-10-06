import os
from flask import Flask, request
import json
import mysql.connector


app = Flask(__name__)

@app.get("/getcustomers", strict_slashes=False)
def get_customers():
    DB_UNIX_SOCKET_DIR="/cloudsql"
    # DB_HOST=os.getenv("DB_HOST","localhost")
    CLOUD_SQL_CONNECTION_NAME=os.getenv("CLOUD_SQL_CONNECTION_NAME")
    DB_USER=os.getenv("DB_USER","root")
    DB_PASSWORD=os.getenv("DB_PASSWORD","passw0rd")
    # DB_HOST=os.getenv("DB_HOST","localhost")
    # DB_USER=os.getenv("DB_USER","root")
    # DB_PASSWORD=os.getenv("DB_PASSWORD","passw0rd")

    query = ("SELECT * FROM customers")
    
    with mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, unix_socket=f"{DB_UNIX_SOCKET_DIR}/{CLOUD_SQL_CONNECTION_NAME}", database='customer_mgmt') as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(query)
            result = cur.fetchall()
            print(result)
            return result

if __name__ == "__main__":
    get_customers()