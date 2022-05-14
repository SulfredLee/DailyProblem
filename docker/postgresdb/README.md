# Docker-compose for PostgresDB

## To use this project

```
# Stop
docker-compose --env-file ./dev_non_persistent/.env down -v
# Start
docker-compose --env-file ./dev_non_persistent/.env up -d
```

Ref: [bitnami](https://github.com/bitnami/bitnami-docker-postgresql)

## .env File

.env file is used for setting up the Environment Variables inside the docker-container

| ENV Variable | Default | Meaning |
| --- | --- | --- |
| SERVICE_NAME | NO_DEFAULT | The name of the service that spawn the postgresDB |
| POSTGRESQL_VERSION | 14 | The version of the postgres db used |
| POSTGRESQL_MASTER_PERSISTENCE_PATH | pg_0 | Path to volumn to store db data, default will store value in container |
| POSTGRESQL_MASTER_USERNAME | postgres | User name for master PG |
| POSTGRESQL_MASTER_PASSWORD | postgres | Password for master PG |
| POSTGRESQL_MASTER_PORT | 25432 | Port for master PG |
| POSTGRESQL_REPLICATION_USER | replication_user | User name for replication PG|
| POSTGRESQL_REPLICATION_PASSWORD | replication_password | Password for replication PG |
| POSTGRESQL_REPLICATION_PORT | 25433 | Port for replication PG |
| POSTGRESQL_ADMIN_PORT | 25480 | Admin port for management |

