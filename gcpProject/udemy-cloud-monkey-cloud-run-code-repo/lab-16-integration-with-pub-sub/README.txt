┌───────────────────────────────────────────────────────────────────────────────────┐
|           Integrating Cloud Run Service with Pub/Sub                              |
└───────────────────────────────────────────────────────────────────────────────────┘
Push Code To Git Repo
---------------------
Open Command prompt and CD into code-root directory
Commands:
    git add .
    git commit -m "lab-16-integration-with-pub-sub"
    git push

Create Build Trigger From UI
----------------------------
Go to Cloud Build
Click on Triggers
Click on Setup Build Triggers
Name: lab-16-load-customers-svc-tr
Region: us-central1
Event: Manual Invocation
Repository Generation: 2nd gen
Repository: udemy-cloud-monkey-cloud-run-code-repo
Branch: main
Configuration: Cloud Build configuration file (yaml or json)
Cloud Build Configuration File Location: lab-16-integration-with-pub-sub/buildconfig/cloudbuild.yaml
Service Account: sa-cloud-build


Go to UI and Invoke the Build Trigger
-------------------------------------
Go to Cloud Build
Click on Triggers
Look for trigger named lab-16-load-customers-svc-tr and click Run

Create Service Account
----------------------
Go to IAM & Admin
Click on Service Accounts
Click on Create Service Account
    Service Account Name: sa-load-customers-pubsub
    Service Account Id: sa-load-customers-pubsub
    Role: Cloud Run Invoker


Create Pub Sub Message Schema
-----------------------------

Go to Pub/Sub
Click on Schemas
Click on Create Schema
    Schema ID: load-customers-pubsub-message-schema
    Schema Type: Avro
    Schema: {
   "type":"array",
   "name":"customers",
   "items":{
      "name":"customer",
      "type":"record",
      "fields":[
         {
            "name":"customer_id",
            "type":"int"
         },
         {
            "name":"name",
            "type":"string"
         },
         {
            "name":"address",
            "type":"string"
         },
         {
            "name":"city",
            "type":"string"
         },
         {
            "name":"state",
            "type":"string"
         },
         {
            "name":"zipcode",
            "type":"string"
         },
         {
            "name":"country",
            "type":"string"
         },
         {
            "name":"entry_type",
            "type":"string"
         }
      ]
   }
}
Click On Validate Defination
Click on Create

Sending a test message
----------------------

Go to Pub/Sub
Click on Schemas
Click on load-customers-pubsub-message-schema
Click on Test Message
Message body: [
{
   "customer_id":11,
   "name":"Colleen Lucht",
   "address":"860 Prospect Valley Road",
   "city":"Los Angeles",
   "state":"California",
   "zipcode":"90017",
   "country":"United States",
   "entry_type":"pubsub"
},
{
   "customer_id":12,
   "name":"Nicholas Newman",
   "address":"3318 Hilltop Haven Drive",
   "city":"Madison",
   "state":"New Jersey",
   "zipcode":"07940",
   "country":"United States",
   "entry_type":"pubsub"
}
]

Click Test

Create Pub Sub Topic
---------------------
Go to Pub/Sub
Click on Topics
Click on Create Topic
    Topic ID: load-customers
    Uncheck Add a default subscription
    Check Use a Schema
        Schema: load-customers-pubsub-message-schema
    Click Create


Create Subscription
--------------------
Go to Pub/Sub
Click on Topics
Click on load-customers
Click on Create Subscription
    Subscription ID: load-customers-svc-sub
    Delivery Type: Push
    Endpoint URL: https://lab-16-load-customers-svc-PROJECT_HASH-uc.a.run.app/loadcustomers
    Check Enable Authentication
        Service Account: sa-load-customers-pubsub
    Message Retention Duration: 0 Days, 0 Hours, 10 Minutes
    Click Create


Publish message
---------------
Go to Pub/Sub
Click on Topics
Click on load-customers
Click on Messages
Click on PUBLISH MESSAGE
    Message Body: [
{
   "customer_id":11,
   "name":"Colleen Lucht",
   "address":"860 Prospect Valley Road",
   "city":"Los Angeles",
   "state":"California",
   "zipcode":"90017",
   "country":"United States",
   "entry_type":"pubsub"
},
{
   "customer_id":12,
   "name":"Nicholas Newman",
   "address":"3318 Hilltop Haven Drive",
   "city":"Madison",
   "state":"New Jersey",
   "zipcode":"07940",
   "country":"United States",
   "entry_type":"pubsub"
}
]

Click on Publish