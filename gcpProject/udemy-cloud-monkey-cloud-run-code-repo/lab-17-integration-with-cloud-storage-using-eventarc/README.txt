┌───────────────────────────────────────────────────────────────────────────────────┐
|           Integrating Cloud Run Service with Eventarc (Cloud Storage Events)      |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-17-integration-with-cloud-storage-using-eventarc"
    git push

Enable APIs & Services
----------------------

Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Eventarc API
    Eventarc Publishing API

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-17-load-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-17-integration-with-cloud-storage-using-eventarc/buildconfig/cloudbuild.yaml
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-17-load-customers-svc-tr and click Run

Create Bucket
-----------------------------

Go to Cloud Storage
Click on Buckets
Click on Create 
    Name: bucket-incoming-customers-PLACEHOLDER_PROJECT_ID
    Location type: Region
        us-central1
    Storage Class: Standard


Assign permissions to Service Account associated with Cloud Storage
-------------------------------------------------------------------
Go to Cloud Storage
Click on Settings
Scroll down to Cloud Storage Service Account
Copy Service Account email

Assign Permissions to Service Account associated with Cloud Storage
-------------------------------------------------------------------
Go to IAM
Click on IAM on the left
Click on Grant Access
   Principal: <Service Account associated with Cloud Storage>
   Role: 
      Pub/Sub Publisher

Assign Permissions to Service Account Cloud Run Service
-------------------------------------------------------
Go to IAM
Click on IAM on the left
Look for sa-customers-svc Service account
click on Edit Principal
Click on Add Another Role
   Role: Storage Object Viewer


Create Service Account for Eventarc Trigger
-----------------------------------------
Go to IAM
Click on Service Accounts
Click on Create Service Account
   Name: sa-load-customers-eventarc
   Roles:
      Eventarc Event Receiver
      Service Account Token Creator
      Cloud Run Invoker

Wait for few minutes as it takes some time for the permissions to propogate to Eventarc 

Create Event
------------
Go to Eventarc
Click on Triggers
Click on Create Trigger
   Trigger Name: customers-data-file-arrived
   Trigger Type: Google sources
   Event Provider: Cloud Storage
   Event: google.cloud.storage.object.v1.finalized
   Bucket: bucket-incoming-customers-PLACEHOLDER_PROJECT_ID
   Service Account: sa-load-customers-eventarc
   Event Destination: Cloud Run
   Select a Cloud Run Service: lab-17-load-customers-svc
   Service URL Path: /loadcustomers


Upload customers.json file to the bucket-incoming-customers-PLACEHOLDER_PROJECT_ID bucket