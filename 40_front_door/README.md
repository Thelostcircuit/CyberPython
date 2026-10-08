# 40 // FRONT DOOR

```
[CHEESE SHOP] purchase: flask ── host: the Adder's Nest back-room server ── audience: 9,402 people waking up
```

**Package:** [`Flask`](https://flask.palletsprojects.com/): a small, readable web framework (WSGI, like ch 26's `wsgiref` app, with a lot more help).

When the released minds come online on the holding server, the first thing each one sees
will be a page: *You're safe. You've been asleep. Here's what day it is. Check in so your
people can find you.* Behind that page is a small API that the crew and the holding server will
use: check-ins, a roster, a status endpoint.

> **WENSLEYDALE:** Flask gets out of your way, sir. A function, a decorator with a URL, and
> you've got a web app. It grows as far as you need: blueprints, sessions, templates, error
> handlers. Very popular with people who like to know what their code is doing.
>
> **MONTY:** And it's WSGI underneath, the same interface as our little `hello_app` in ch 26.
> Everything connects.

---

## ▓ TECH BRIEFING

### An app and routes

```python
from flask import Flask, jsonify, request, abort, session, render_template_string

app = Flask(__name__)

@app.get("/")
def home():
    return "<h1>You're safe.</h1>"          # a str becomes an HTML response

@app.get("/api/status")
def status():
    return {"status": "up"}                  # a dict becomes JSON (or use jsonify)

@app.post("/api/checkin")
def checkin():
    data = request.get_json(silent=True) or {}
    if "id" not in data:
        abort(400)
    return {"ok": True}, 201                 # (body, status) tuples

@app.get("/api/checkin/<subject_id>")        # URL variables; <int:n> converts too
def lookup(subject_id): ...
```

`request.args` holds query parameters, `request.form` form fields, `request.get_json()` a JSON
body, and `request.headers` the headers. Run a dev server with `flask --app module run`, or
`app.run(debug=True)` (never in production).

### The application factory, config, and blueprints

```python
from flask import Blueprint, current_app
api = Blueprint("api", __name__, url_prefix="/api")

@api.get("/roster")
def roster():
    return current_app.config["ROSTER"]      # current_app = the app handling this request

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY="dev", ROSTER={})
    if test_config: app.config.update(test_config)
    app.register_blueprint(api)
    return app
```

A factory makes a fresh, independent app each time, which is exactly what tests need.

### Errors, sessions, templates

```python
@app.errorhandler(404)
def not_found(e):
    return {"error": "not found"}, 404

session["user"] = "adder"      # a signed cookie; needs app.config["SECRET_KEY"]

render_template_string("<p>Welcome back, {{ name }}.</p>", name=request.args.get("name", "friend"))
# Jinja2 templates AUTO-ESCAPE: <script> in `name` is shown as text, not run
# (real apps keep templates in templates/*.html and use render_template)
```

### Testing

```python
client = create_app({"TESTING": True}).test_client()
r = client.post("/api/checkin", json={"id": "OS-ENG-4471", "name": "Iris"})
r.status_code, r.get_json(), r.get_data(as_text=True)
```

---

## ▓ THE JOB

In `job.py`, build **`create_app(test_config=None)`**, a Flask factory:

- `SECRET_KEY` defaults to `"dev"`, and each app gets its own empty check-in store in `app.config["CHECKINS"]`.
- `GET /?name=...`: an HTML welcome built with `render_template_string` (auto-escaped).
- An **`api` blueprint** at `/api`:
  - `GET /api/status` → `{"status": "up", "checked_in": N}`
  - `POST /api/checkin` (JSON `id`, `name`, `wing`) → 201 with the record, 400 if a field is missing, 409 if that id already checked in.
  - `GET /api/checkin/<id>` → the record, or a 404.
  - `GET /api/roster?wing=C` → the checked-in records (optionally filtered by wing), sorted by id.
  - `POST /api/login` (JSON `user`) → stores the user in the `session`. `GET /api/me` → `{"user": ...}`, or 401.
- Every 404 answers with the JSON `{"error": "not found"}`.

The docstring in `job.py` has the exact shapes.
