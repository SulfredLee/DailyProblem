┌───────────────────────────────────────────────────────────────────────────────────┐
|           Talking to Cloud SQL using SQL Connection using Direct VPC Egress       |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-15-integration-cloud-sql-cloud-sql-connection-over-direct-vpc-egress"
    git push

Enable APIs & Services
-----------------------
Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Cloud SQL Admin API


Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-15-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-15-integration-cloud-sql-cloud-sql-connection-over-direct-vpc-egress/buildconfig/cloudbuild.yaml
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-15-get-customers-svc-tr and click Run
