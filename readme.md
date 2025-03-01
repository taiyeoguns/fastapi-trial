# Fastapi-Trial

Fastapi application to show typical Create, Read, Update, Delete (CRUD) operations.

## Requirements

- Python 3.11
- Fastapi
- Postgres database
- Pytest
- Docker

## Installation

### Clone Project

```sh
git clone https://github.com/taiyeoguns/fastapi-trial.git
```

### Install Requirements

With a [virtualenv](https://virtualenv.pypa.io/) already set-up, install the requirements with pip:

```sh
make install
```

### Add details in `.env` file

Create `.env` file from example file and maintain necessary details in it.

```sh
cp .env.example .env
```

### Set up database

SQLAlchemy is used to model the data and alembic is used to keep the database up-to-date with migrations.

To setup a local database, fill in database details in `.env` file from earlier or set up environment variables. Ensure the database and user defined in `.env` is already created in Postgres.

For initial database setup, run the following commands:

```sh
make db-upgrade
```

Subsequently, after making any changes to the database models, run the following commands:

```sh
make db-migrate
make db-upgrade
```

### Seeding the database

To seed the database with initial data, run:

```sh
make seed
```

### Run the application

Activate the virtual environment and start the application by running:

```sh
make run
```

### Authenticating API requests

To authenticate API requests, pass a valid API key as a header with key `X-Api-Key`.

### Tests

In command prompt, run:

```sh
make test
```

### Run application with Docker

Ensure database details are added to `.env` file from earlier.

The following environment variables should be set in the `.env` file even if they do not 'exist', the docker postgres image will use them for setting up the container -
`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

With Docker and Docker Compose set up, run:

```sh
make docker-run
```

Thereafter, application should be available at `http://localhost:8000`
