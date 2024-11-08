#!/bin/bash

docker pull postgres:13.16

docker run -d \
--name postgres_test \
-e POSTGRES_PASSWORD=mysecretpassword \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-p 5432:5432 \
-v /home/user/db_data/postgresql/data:/var/lib/postgresql/data \
postgres:13.16

