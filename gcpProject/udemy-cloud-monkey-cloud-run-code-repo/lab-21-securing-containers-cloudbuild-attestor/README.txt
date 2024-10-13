┌───────────────────────────────────────────────────────────────┐
|           Securing Artifacts using cloud-build-attestor       |
└───────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-21-securing-containers-cloudbuild-attestor"
    git push

Enable APIs & Services
-----------------------
Go to APIs & Services
Click on Enable APIs & Services
APIs to Enable:
    Container Analysis API
    Binary Authorization API

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Create Trigger
Name: lab-21-get-customers-svc-build-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 1st gen
Repository: cloud-monkey-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-21-securing-containers-cloudbuild-attestor/buildconfig/cloudbuild-build.yaml

Service Account: sa-cloud-build-svc


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-21-get-customers-svc-build-tr and click Run


Modify default binary authorization policy
------------------------------------------
Go to Security
Click on Binary Authorization
Go to Policy
Click on Edit Policy
Select Require attestations
Click Add Attestors
    Select built-by-cloud-build
Click on Save Policy


Create Deploy Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Create Trigger
Name: lab-21-get-customers-svc-deploy-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 1st gen
Repository: cloud-monkey-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-21-securing-containers-cloudbuild-attestor/buildconfig/cloudbuild-deploy.yaml
Substitution variables
    Click on ADD VARIABLE
        Variable 1:
            _ACCOUNTBALANCE_CLOUD_RUN_SERVICE_URL
        Value: Account balance Cloud Run Service URL

Service Account: sa-cloud-build-svc

Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-21-get-customers-svc-deploy-tr and click Run

Verify
------
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t us-central1-docker.pkg.dev/PLACEHOLDER_PROJECT_ID/cloud-monkey-artifact-registry/lab-21-get-customers-svc-img ./lab-21-securing-containers-cloudbuild-attestor/microservices/customers/
docker push --all-tags us-central1-docker.pkg.dev/PLACEHOLDER_PROJECT_ID/cloud-monkey-artifact-registry/lab-21-get-customers-svc-img

Redeploy the service
--------------------
Go to Cloud Build
Click on Triggers
Click Run next to lab-21-get-customers-svc-deploy-tr
