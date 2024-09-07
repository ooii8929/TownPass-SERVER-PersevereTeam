# Web Server

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
python -m pip install -r requirements.txt

gunicorn 'src.app:app' --bind=0.0.0.0:8000

# watch mode
watchmedo auto-restart --patterns="*.py" --recursive -- gunicorn -w 4 -b 127.0.0.1:8000 src.app:app
```
