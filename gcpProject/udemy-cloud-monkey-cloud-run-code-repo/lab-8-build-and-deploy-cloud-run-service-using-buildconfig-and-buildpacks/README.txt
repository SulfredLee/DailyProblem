┌───────────────────────────────────────────────────────────────────────────────────┐
|           Cloud Run Service using Cloudbuild Config and Buildpacks                |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-8-build-and-deploy-cloud-run-service-using-buildconfig-and-buildpacks"
    git push

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-08-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-8-build-and-deploy-cloud-run-service-using-buildconfig-and-buildpacks/buildconfig/cloudbuild.yaml
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-08-get-customers-svc-tr and click Run

Invoke the Build Trigger From CLI
---------------------------------
gcloud builds triggers run lab-08-get-customers-svc-tr