# Running the App

The template includes a Docker Compose configuration, which allows you to easily run the application together with all
required services.

The easiest way to start the application in a development or testing environment is:

```bash
make run
```

## Database Migrations

To create a new database migration, run:

```bash
make migrate
```

To apply pending migrations:

```bash
make migrate_up
```

## Environment Files

The project uses separate environment files depending on how the application is executed:

* **`.env`** — used by the application when running inside Docker containers.
* **`.env.local`** — used when running the application directly on the host machine and when creating or applying
  database migrations locally.
* **`.env.test`** — used when running tests. Tests use a separate PostgreSQL database instance and are executed outside
  the application container.
  utside the container