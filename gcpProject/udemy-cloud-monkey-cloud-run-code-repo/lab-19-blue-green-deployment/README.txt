┌───────────────────────────────────────┐
|           Blue Green Deployment       |
└───────────────────────────────────────┘

Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-19-blue-green-deployment-blue"
    git push

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-19-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-19-blue-green-deployment/buildconfig/cloudbuild-customers.yaml
Service Account: sa-cloud-build

Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-19-get-customers-svc-tr and click Run


Make Code Change
----------------
Copy content from customers-green/main.py and paste it in customers/main.py

Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-19-blue-green-deployment-green"
    git push


Create Build Trigger From UI (Green)
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-19-get-customers-svc-green-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-19-blue-green-deployment/buildconfig/cloudbuild-customers-green.yaml
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
Look for trigger named lab-19-get-customers-svc-green-tr and click Run

Test with green URL
-------------------

Change Traffic Pattern
----------------------
Go to Clour Run
Click on lab-19-get-customers-svc
Click on Revisions
Click on Manage Traffic
Revision 2: Select green
Traffic 2: Enter 50
Click Save


Change Traffic Pattern
----------------------
Go to Clour Run
Click on lab-19-get-customers-svc
Click on Revisions
Click on Manage Traffic
Delete Revision 1
Change Traffic to 100 for green

