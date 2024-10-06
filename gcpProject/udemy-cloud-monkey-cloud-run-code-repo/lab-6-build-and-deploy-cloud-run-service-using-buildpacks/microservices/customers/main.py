from flask import Flask, request

app = Flask(__name__)


@app.get("/getcustomers", strict_slashes=False)
def get_customers():
    customers = get_customers_data()
    return customers

def get_customers_data():
    customers = [
    {'customer_id': 1, 'name': 'Sara White', 'address': '5866 Fuller Road', 'city': 'Henryport', 'state': 'Maryland', 'zipcode': '28764', 'country': 'United States'},
    {'customer_id': 2, 'name': 'Brian Davenport', 'address': '2139 Mcguire Estates Apt. 391', 'city': 'North Peter', 'state': 'Alaska', 'zipcode': '85682', 'country': 'United States'},
    {'customer_id': 3, 'name': 'Donald Poole', 'address': '123 Karen Lights', 'city': 'Teresahaven', 'state': 'West Virginia', 'zipcode': '17084', 'country': 'United States'},
    {'customer_id': 4, 'name': 'Casey Conner', 'address': '18792 Gibson Throughway Apt. 646', 'city': 'West Michaelfort', 'state': 'Florida', 'zipcode': '37673', 'country': 'United States'},
    {'customer_id': 5, 'name': 'Kathy Hicks', 'address': '447 Michael Trail Suite 172', 'city': 'Ericside', 'state': 'Hawaii', 'zipcode': '93229', 'country': 'United States'}
    ]
    return customers

