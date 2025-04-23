# How to run locally
We are using `Python 3.12.2` for this project.

1. Generate environment variables

```bash
cp env/db.example.env env/db.env && cp env/web.example.env env/web.env
```

Then you can open `env/db.env` and `env/web.env` file and edit creds as per your need.

2. Run local server

```bash
docker compose up --build
```

NOTE: For first time it might throw error as database is not connected and django is trying to connect db. If that happens, just hit Ctrl + C and rerun the above command it will fix.

3. Run db migrations

```bash
docker compose exec web python manage.py migrate
```

Now you can go to `http://localhost:8000` to open the web app.

You can use `docker compose down` command to take down server or `Ctrl + C` command.