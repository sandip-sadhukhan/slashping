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
cp .deafult.env .env
```

Then edit the `.env` file if you want.

6. Run the local server

```bash
python manage.py runserver
```
