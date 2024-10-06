┌──────────────────────────────────────────────────────────────┐
|           Setup Cloud SQL Instance                           |
└──────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
|           Prep Work                                    |
|────────────────────────────────────────────────────────|
|                                                        |
|Replace PLACEHOLDER_PROJECT_ID with Project Id in       |
|   this file                                            |
└────────────────────────────────────────────────────────┘

Enable APIs & Services
-----------------------
Go to APIs & Services
Click on ENABLE APIS AND SERVICES
Enable below APIs:
    Compute Engine API
    Cloud SQL



Setup Cloud SQL Instance
------------------------
Go to SQL
Click on Create instance
Click on Choose MySQL
    Instance Id: customers-db-instance
    Password: password123
    Database Version: MYSQL 8.0
    Cloud SQL edition: Enterprise
    Edition: Sandbox
    Region: us-central1
    Zonal availability: Single Zone
    Expand SHOW CONFIGURATION OPTIONS
        Expand Machine Configuration
            Machine shapes:
                Shared Core
                1 vCPU, 0.614 GB
        Expand Connections:
            Instance IP assignment:
                Select Public IP if not already selected
            Authorized networks:
                Click on ADD A NETWORK
                    Name: allow-all
                    Network: 0.0.0.0/0
        Expand Data Protection:
            Uncheck Automate daily backups
            Uncheck Enable deletion protection


Get Service Account for Cloud SQL Instance
------------------------------------------
Go to Cloud SQL
Click on customers-db-instance
Scroll down to get the Service account
Copy and paste in the notes

Assign permissions Cloud SQL Instance Service Account to read from Cloud Storage
--------------------------------------------------------------------------------
Go to IAM
Select IAM from the left menu
Click on Grant Access
    Add principals
        New Principal: <<Cloud SQL Instance Service Account email From the Notes>>
    Roles:
        Storage Object Viewer
Click Save

Import Initial Data into Cloud SQL Instance
-------------------------------------------
Go to Cloud Storage
Select Buckets from the left menu
Click on Create
    Name: bucket-import-mysql-data-PLACEHOLDER_PROJECT_ID
    Location type: Region
        us-central1
    Storage Class: Standard

Upload sql-dump-lab-10.sql file to the bucket


Import Data into Cloud SQL Instance
-----------------------------------
Go to Cloud SQL
Click on customers-db-instance
Click on IMPORT
    Source: Browse to bucket-import-mysql-data-PLACEHOLDER_PROJECT_ID and select sql-dump-lab-10.sql
    File FormatL SQL
    Destination:
        Database: Specified in the file
    Click Import

Verify
------
Go to Cloud SQL
Click on customers-db-instance
Click on Databases
Ensure there is an entry for customer_mgmt database

Get Public IP for Cloud SQL Instance
------------------------------------------
Go to Cloud SQL
Click on customers-db-instance
Scroll down to get the Public IP Address
Copy and paste in the notes
