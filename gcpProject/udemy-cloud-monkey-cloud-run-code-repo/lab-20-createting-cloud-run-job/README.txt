┌─────────────────────────────────────────┐
|           Deploying Cloud Run Job       |
└─────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-20-createting-cloud-run-job"
    git push

Create bucket for Outgoing customers data
-----------------------------------------
Go to Cloud Storage
Click on Buckets
Click on Create
    Name: bucket-outgoing-customers-cloud-run-demo-396721
    Location type: Regiona
        Region: us-central1
Click on Create

Add permissions to Service Account
---------------------------------
Go to IAM & Admin
Click on IAM
Look for sa-customers-svc and click on Edit Principal
Add Role:
    Role: Storage Admin

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-20-dump-customers-job-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-20-createting-cloud-run-job/buildconfig/cloudbuild.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _ACCOUNTBALANCE_CLOUD_RUN_SERVICE_URL
        Value 1: Account balance Cloud Run Service URL From Lab 18

Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-20-dump-customers-job-tr and click Run

Invoke Cloud Run Job
--------------------
Go to Cloud Run
Click on Jobs
Click on Job: lab-20-get-customers-job
Click on Execute

Enable APIs & Services
----------------------
Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Cloud Scheduler API

Create Schedule
---------------
Go to Cloud Run
Click on Jobs
Click on lab-20-get-customers-job
Click on Triggers
Click on Add Scheduled Trigger
    Name: lab-20-get-customers-job-scheduler-trigger-every-5-minutes
    Region: us-central1
    Frequency: */5 * * * *
    Timezone: UTC