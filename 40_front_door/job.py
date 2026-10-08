"""40 // FRONT DOOR: the holding server's welcome page and API, in Flask.

create_app(test_config=None) must return a NEW Flask app each call, with:
  config SECRET_KEY="dev" and CHECKINS={} (a fresh dict per app), then test_config applied.

  GET  /                   -> HTML from render_template_string:
                              "<h1>You're safe.</h1><p>Welcome back, {{ name }}.</p>"
                              name = ?name=... or "friend" (auto-escaped by Jinja)
  Blueprint "api", url_prefix "/api":
  GET  /api/status         -> {"status": "up", "checked_in": <number of check-ins>}
  POST /api/checkin        -> JSON body with "id", "name", "wing" (all required)
                              missing any -> 400 {"error": "missing field"}
                              id already present -> 409 {"error": "already checked in"}
                              else store {"id", "name", "wing"} under the id -> 201 with that record
  GET  /api/checkin/<id>   -> 200 record, or 404 {"error": "not found"}
  GET  /api/roster         -> {"roster": [records sorted by id]}; ?wing=C filters by wing
  POST /api/login          -> JSON {"user": ...}; store it in session["user"]; 200 {"ok": true}
  GET  /api/me             -> {"user": session user} or 401 {"error": "not logged in"}
  Any 404 anywhere         -> JSON {"error": "not found"} (register an errorhandler)
"""

from flask import Blueprint, Flask, current_app, render_template_string, request, session

# TODO: create the "api" blueprint and its routes here


def create_app(test_config: dict | None = None) -> Flask:
    raise NotImplementedError("TODO")
