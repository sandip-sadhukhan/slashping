# How to run locally
We are using `Python 3.12.2` for this project.

1. Create a virtual env.

```bash
python3 -m venv venv
```

2. Activate the venv

```bash
source venv/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Build the tailwind css

```bash
npm install
npm run watch:css
```

5. Create the `.env` file

```bash
cp .env.example .env
```

Then edit the `.env` file if you want.

6. Run all migrations
```bash
python manage.py migrate
```

7. Run redis-server
```bash
redis-server
```

8. Run celery beat and celery worker
```bash
celery -A core worker -l info
celery -A core beat -l info
```

9. Run mailhog
```bash
mailhog # if exe is setup
# or for macos
brew services start mailhog
```

10. Run the local server

```bash
python manage.py runserver
```
