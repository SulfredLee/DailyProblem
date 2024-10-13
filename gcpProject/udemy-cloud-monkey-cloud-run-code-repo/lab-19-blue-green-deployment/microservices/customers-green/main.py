import os
from flask import Flask, request
import json
import mysql.connector
import google.oauth2.id_token
import google.auth.transport.requests
import urllib


app = Flask(__name__)

accountbalance_cloud_run_service_url = f"{os.environ['ACCOUNTBALANCE_CLOUD_RUN_SERVICE_URL']}/getaccountbalance"
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

    accountbalance = get_accountbalance()
    print(accountbalance)

    query = ("SELECT * FROM customers")
    
    with mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, unix_socket=f"{DB_UNIX_SOCKET_DIR}/{CLOUD_SQL_CONNECTION_NAME}", database='customer_mgmt') as conn:
        with conn.cursor(dictionary=True) as cur:
            cur.execute(query)
            result = cur.fetchall()
            print(result)
            for customer in result:
                customer_id = customer["customer_id"]
                account_balance = next((c for c in accountbalance["accountbalance"] if c["customer_id"] == customer_id), None)
                if account_balance:
                    customer["account_balance"] = account_balance["account_balance"]
            return result

def get_accountbalance():
    accountbalance_cloud_run_service_audience = accountbalance_cloud_run_service_url
    accountbalance_cloud_run_service_auth_req = google.auth.transport.requests.Request()
    accountbalance_cloud_run_service_id_token = google.oauth2.id_token.fetch_id_token(accountbalance_cloud_run_service_auth_req, accountbalance_cloud_run_service_audience)

    print(f"getting account balance from {accountbalance_cloud_run_service_url}")
    accountbalance_cloud_run_service_request = urllib.request.Request(f"{accountbalance_cloud_run_service_url}")
    accountbalance_cloud_run_service_request.add_header("Authorization", f"Bearer {accountbalance_cloud_run_service_id_token}")
    accountbalance_cloud_run_service_response = urllib.request.urlopen(accountbalance_cloud_run_service_request,timeout=15)

    accountbalance = json.loads(accountbalance_cloud_run_service_response.read())
    return accountbalance

if __name__ == "__main__":
    get_customers()