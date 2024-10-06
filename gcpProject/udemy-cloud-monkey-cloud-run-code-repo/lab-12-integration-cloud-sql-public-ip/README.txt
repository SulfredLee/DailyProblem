┌───────────────────────────────────────────────────────────────────────────────────┐
|           Talking to Cloud SQL over Public IP                                     |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-12-integration-cloud-sql-public-ip"
    git push

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-12-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-12-integration-cloud-sql-public-ip/buildconfig/cloudbuild.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _DB_HOST
        Value 1:
            <Cloud SQL Instance Public IP Address from Notes>
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-12-get-customers-svc-tr and click Run
