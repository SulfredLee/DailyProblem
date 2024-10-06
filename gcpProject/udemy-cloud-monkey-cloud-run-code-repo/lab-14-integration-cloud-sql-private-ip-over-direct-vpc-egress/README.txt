
┌───────────────────────────────────────────────────────────────────────────────────┐
|           Talking to Cloud SQL over Priave IP using Direct VPC Egress             |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-14-integration-cloud-sql-private-ip-over-direct-vpc-egress"
    git push


Add Cloud SQL Client IAM Role to sa-customers-svc Service Account
-----------------------------------------------------------------
Go to IAM & Admin
Click on IAM
Click on Grant Access
Look for sa-customers-svc and click on Edit Principal
Click on Add Another Role
    Role:
        Cloud SQL Client

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-14-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-14-integration-cloud-sql-private-ip-over-direct-vpc-egress/buildconfig/cloudbuild.yaml
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
Look for trigger named lab-14-get-customers-svc-tr and click Run
