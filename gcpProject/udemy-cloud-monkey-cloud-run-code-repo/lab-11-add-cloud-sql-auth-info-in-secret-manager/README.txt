┌───────────────────────────────────────────────────────────────────────────────────┐
|           Add Cloud SQL Auth Details to Secret Manager                            |
└───────────────────────────────────────────────────────────────────────────────────┘

Add Cloud SQL Auth Information to Secret Manager
------------------------------------------------
Go to Secret Manager
Click on Create Secret
   Name: db-user
   Value: root
Click on Create Secret

Go to Secret Manager
Click on Create Secret
   Name: db-password
   Value: password123
Click on Create Secret

Grant Service Account permission to read Secrets
------------------------------------------------
Go to IAM & Admin
Click on IAM
Click on Grant Access
    New Principal: sa-customers-svc
    Role: Secret Manager Secret Accessor