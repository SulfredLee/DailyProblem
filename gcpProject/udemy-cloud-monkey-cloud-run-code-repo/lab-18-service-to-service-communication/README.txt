┌───────────────────────────────────────────────────────────────────────────────────┐
|           Cloud Run Service to Service Communication Securely                     |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-18-service-to-service-communication"
    git push

Upload SQL Dump file to Cloud Storage
-------------------------------------
Go to Cloud Storage
Click on Buckets
Click on bucket-import-mysql-data-PLACEHOLDER_PROJECT_ID
Upload sql-dump-lab-18.sql file

Import Data into Cloud SQL
--------------------------

Go to Cloud SQL
Click on  customers-db-instance
Click on IMPORT
Browse to bucket-import-mysql-data-PLACEHOLDER_PROJECT_ID/sql-dump-lab-18.sql
Click Import

Create Service Account for Accountbalance Service
-------------------------------------------------
Go to IAM & Admin
Click on Service Accounts
Click on Create Service Account
    Service Account Name: sa-accountbalance-svc
    Service Account Id: sa-accountbalance-svc
    Roles:
        Cloud SQL Client
        Secret Manager Secret Accessor

Create Build Trigger From UI (Account Balance)
----------------------------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-18-get-accountbalance-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-18-service-to-service-communication/buildconfig/cloudbuild-accountbalance.yaml
Service Account: sa-cloud-build

Go to UI and Invoke the Build Trigger (Account Balance)
-------------------------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-18-get-accountbalance-svc-tr and click Run

Authorize sa-customers-svc Service Account to invoke getaccountbalance Cloud Run Service
-----------------------------------------------------------------------------------------
Go to IAM
Click on IAM
Look for sa-customers-svc
Click on Edit Principal
    Role: Cloud Run Invoker


Create Build Trigger From UI (Customers)
----------------------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-18-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-18-service-to-service-communication/buildconfig/cloudbuild-customers.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _ACCOUNTBALANCE_CLOUD_RUN_SERVICE_URL
        Value: Account balance Cloud Run Service URL
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-18-get-customers-svc-tr and click Run

