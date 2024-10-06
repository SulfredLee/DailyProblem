┌───────────────────────────────────────────────────────────────────────────────────┐
|               Create Service Accounts & Assign Required Permissions               |
└───────────────────────────────────────────────────────────────────────────────────┘

Create Service Account for Cloud Build
--------------------------------------
Go to IAM & Admin
Click on Service Accounts
Click on Create Service Account
    Service Account Name: sa-cloud-build
    Service Account Id: sa-cloud-build

Create Service Account for Cloud Run Service
--------------------------------------------
Go to IAM & Admin
Click on Service Accounts
Click on Create Service Account
    Service Account Name: sa-customers-svc
    Service Account Id: sa-customers-svc

Assign Permissions to Service Account
--------------------------------------
Go to IAM & Admin
Click on IAM
Click on Grant Access
Add principals
    New Principal: sa-cloud-build
Roles:
    Logs Writer
    Artifact Registry Writer
    Cloud Run Admin
    Service Account User

    Not Required unless using Cloud Source Repositories:
    Source Repository Reader