
┌───────────────────────────────────────────────────────────────────────────────────┐
|                           Cloud Run Service using Buildpacks                      |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-6-build-and-deploy-cloud-run-service-using-buildpacks"
    git push

Create Build Trigger
--------------------
Go to Cloud Build
Click on Dashboard
Click on Setup Build Triggers
Name: lab-06-get-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Buildpacks
Build Directory: lab-6-build-and-deploy-cloud-run-service-using-buildpacks/microservices/customers
Image Name: us-central1-docker.pkg.dev/$PROJECT_ID/cloud-monkey-artifact-registry/lab-06-get-customers-svc-img:latest
Builder Image: gcr.io/buildpacks/builder

Invoke Build Trigger from UI
----------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-06-get-customers-svc-tr and click Run


Deploy Cloud Run Service
-----------------------
Go to Cloud Run
Click on Create Service
Container Image URL: Browse to Artifact Regitry and Select the image for lab-06-get-customers-svc-img
Service Name: lab-06-get-customers-svc
Region: us-central1
Minimum Number of Instances: 0
Maximum Number of Instances: 1
Authentication: Allow unauthenticated invocations
Expand Container, Networking, Security
Select Container Tab
    Capacity: 256miB
    CPU: 1
    Execution environment: Default
Click Create

