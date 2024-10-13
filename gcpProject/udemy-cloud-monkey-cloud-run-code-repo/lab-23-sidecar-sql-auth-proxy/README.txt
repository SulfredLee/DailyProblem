┌───────────────────────────────────────────────────────────────┐
|           Sidecar Pattern (Cloud SQL Auth Proxy)              |
└───────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-23-sidecar-sql-auth-proxy"
    git push

Enable APIs & Services
-----------------------
Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Cloud Resource Manager API



Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-23-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-23-sidecar-sql-auth-proxy/buildconfig/cloudbuild.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _PROJECT_HASH
        Value: Project hash from the notes

Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-23-get-customers-svc-build-tr and click Run
