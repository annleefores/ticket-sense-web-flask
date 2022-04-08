# ticket-sense-website

Create a project folder and a venv folder within:

```
$ mkdir myproject

$ cd myproject

$ python3 -m venv venv
```

Activate the environment
```
$ . venv/bin/activate
```

Install Flask
```
$ pip install Flask
```

Install dependencies
```
$ pip install python-dotenv && pip install watchdog
```

Create .flaskenv file and add to it:
```
FLASK_APP=app.py
FLASK_ENV=development
```