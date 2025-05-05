# PostgreSQL Docker Setup

This folder contains a Docker setup for running PostgreSQL.

## Configuration

The default configuration:
- PostgreSQL 
- Username: postgres
- Password: postgres
- Database: postgres
- Port: 5432

## Usage

To start the PostgreSQL server:

```bash
cd postgresql
docker-compose up -d
```

To stop the server:

```bash
docker-compose down
```

## Connecting

Connect to the PostgreSQL server using:

```bash
# Using psql CLI
docker exec -it postgres-db psql -U postgres

# Using connection string
postgresql://postgres:postgres@localhost:5432/postgres
```

## Data Persistence

Data is stored in a named Docker volume `postgres-data` which persists between container restarts.

To remove all data:

```bash
docker-compose down -v
``` 