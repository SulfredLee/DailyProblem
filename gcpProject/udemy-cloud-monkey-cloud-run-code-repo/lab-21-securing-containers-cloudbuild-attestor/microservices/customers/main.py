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
    
# from flask import Flask, request

# app = Flask(__name__)


# @app.get("/getcustomers", strict_slashes=False)
# def get_customers():
#     customers = get_customers_data()
#     return customers

# def get_customers_data():
#     customers = [
#     {'customer_id': 1, 'name': 'Sara White', 'address': '5866 Fuller Road', 'city': 'Henryport', 'state': 'Maryland', 'zipcode': '28764', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 2, 'name': 'Brian Davenport', 'address': '2139 Mcguire Estates Apt. 391', 'city': 'North Peter', 'state': 'Alaska', 'zipcode': '85682', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 3, 'name': 'Donald Poole', 'address': '123 Karen Lights', 'city': 'Teresahaven', 'state': 'West Virginia', 'zipcode': '17084', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 4, 'name': 'Casey Conner', 'address': '18792 Gibson Throughway Apt. 646', 'city': 'West Michaelfort', 'state': 'Florida', 'zipcode': '37673', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 5, 'name': 'Kathy Hicks', 'address': '447 Michael Trail Suite 172', 'city': 'Ericside', 'state': 'Hawaii', 'zipcode': '93229', 'country': 'United States', 'entry_type':'manual'}
#     ]
#     return customers

# @app.get("/getcustomer", strict_slashes=False)
# def get_customer():
    
#     request_json = request.get_json(silent=True)
#     request_args = request.args
#     if request_json and 'customerid' in request_json:
#         customer_id = request_json['customerid']
#     elif request_args and 'customerid' in request_args:
#         customer_id = request_args['customerid']
            
#     try:
#         customer_id = int(customer_id)
#     except(Exception):
#         return 'Invalid Customer Id', 400

#     customers = get_customers_data()

#     customer = next((cust for cust in customers if cust['customer_id'] == customer_id), {})
    
#     return customer

# def get_customers_data():
#     customers = [
#     {'customer_id': 1, 'name': 'Sara White', 'address': '5866 Fuller Road', 'city': 'Henryport', 'state': 'Maryland', 'zipcode': '28764', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 2, 'name': 'Brian Davenport', 'address': '2139 Mcguire Estates Apt. 391', 'city': 'North Peter', 'state': 'Alaska', 'zipcode': '85682', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 3, 'name': 'Donald Poole', 'address': '123 Karen Lights', 'city': 'Teresahaven', 'state': 'West Virginia', 'zipcode': '17084', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 4, 'name': 'Casey Conner', 'address': '18792 Gibson Throughway Apt. 646', 'city': 'West Michaelfort', 'state': 'Florida', 'zipcode': '37673', 'country': 'United States', 'entry_type':'manual'},
#     {'customer_id': 5, 'name': 'Kathy Hicks', 'address': '447 Michael Trail Suite 172', 'city': 'Ericside', 'state': 'Hawaii', 'zipcode': '93229', 'country': 'United States', 'entry_type':'manual'}
#     ]
#     return customers


# if __name__ == "__main__":
#     app.run(host="localhost", port=8080, debug=True)