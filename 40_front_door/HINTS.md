# HINTS // 40 FRONT DOOR

## The factory
<details><summary>Hint</summary>

```python
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY="dev", CHECKINS={})   # a NEW dict each call
    if test_config:
        app.config.update(test_config)
    ...routes, error handler...
    app.register_blueprint(api)
    return app
```
</details>

## The blueprint
<details><summary>Hint</summary>

Create `api = Blueprint("api", __name__, url_prefix="/api")` at module level, and decorate the
view functions with `@api.get("/status")` and so on. Inside a view, `current_app.config["CHECKINS"]`
reaches the store of whichever app is handling the request.
</details>

## checkin
<details><summary>Hint</summary>

`data = request.get_json(silent=True) or {}`. `silent=True` returns `None` instead of raising
on a non-JSON body. Check the required fields first, then duplicates. Return `record, 201`.
</details>

## roster
<details><summary>Hint</summary>

Sort `store.values()` by `r["id"]`, then filter if `request.args.get("wing")` is set.
</details>

## login / me
<details><summary>Hint</summary>

`session["user"] = data.get("user")` and `if "user" not in session: return {...}, 401`. The
session is a signed cookie, which the test client keeps between requests.
</details>

## home / 404
<details><summary>Hint</summary>

`render_template_string("<h1>You're safe.</h1><p>Welcome back, {{ name }}.</p>", name=name)`.
Use `@app.errorhandler(404)` inside the factory, and return a `(dict, 404)` tuple.
</details>
