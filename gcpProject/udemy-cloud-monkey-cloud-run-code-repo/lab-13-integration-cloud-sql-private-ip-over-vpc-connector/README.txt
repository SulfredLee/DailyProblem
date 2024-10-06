
┌───────────────────────────────────────────────────────────────────────────────────┐
|           Talking to Cloud SQL over Priave IP using VPC Connector                 |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-13-integration-cloud-sql-private-ip-over-vpc-connector"
    git push


Enable APIs & Services
-----------------------
Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Service Networking API
    Serverless VPC Access API
    

Allocate an IP Range
--------------------
Go to VPC Network
Select VPC Networks
Click on default VPC
Click on PRIVATE SERVICE CONNECTION tab
Click on ALLOCATED IP RANGES FOR SERVICES
Click on ALLOCATE IP RANGE
    Name: cloud-monkey-google-provided-ip-range
    IP range: Automatic
        Prefix Length: 24
Click Allocate

Create Private Connections to Services
-------------------------------------
Go to VPC Network
Select VPC Networks
Click on default VPC
PRIVATE CONNECTIONS TO SERVICES tab
Click on Create Connection
Assigned Allocation:
    Select cloud-monkey-google-provided-ip-range
Click Connect

Create Serverless VPC Access Connector
--------------------------------------
Go to VPC Network
Click on Serverless VPC Access
Click on Create Connector
    Name: serverless-vpc-connector
    Region: us-central1
    Network: default
    Subnet: Custom IP Range
        IP Range: 10.8.0.0
    Expand Scaling Settings
    Scaling Settings:
        Minimum Instances: 2
        Maximum Instances: 3
        Instance Type: e2-micro
Click Create

Modify Cloud SQL Instance to enable Connectivity over Private IP
----------------------------------------------------------------
Go to Cloud SQL
Click on  customers-db-instance
Click on EDIT
Expand Connections
    Instance IP assignment:
        Check Private IP
            Associated networking:
                Network: default
        Uncheck Public IP
    Authorized networks:
        Remove allow-all
Click Save

Get Private IP for Cloud SQL Instance
------------------------------------------
Go to Cloud SQL
Click on customers-db-instance
Scroll down to get the Private IP Address
Copy and paste in the notes

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-13-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-13-integration-cloud-sql-private-ip-over-vpc-connector/buildconfig/cloudbuild.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _DB_HOST
        Value 1:
            <Cloud SQL Instance Private IP Address from Notes>
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-13-get-customers-svc-tr and click Run
