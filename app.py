# /usr/bin/python3
# coding: utf-8

from bottle import get, post, redirect, request, response, jinja2_template as template
import bottle
import peewee
import datetime
from urllib.parse import urljoin
from os import path

import config

from face import Face

#bottle.TEMPLATE_PATH.append(path.join(path.abspath(path.dirname(__file__)), 'templates/'))

@post("/api/slack")
def api_slack():
    text = request.POST.text
    if text == "list":
        characters = Face.select(Face.character).distinct()
        res = ', '.join(list(map(lambda x: x.character, characters)))
        return { "text" : res }
    face = _get_random(text)
    if face:
        return { "text" : _build_url(face.pic_path)}
    else:
        return ""

@get("/character/<character>/random")
def character_random(character):
    face = _get_random(character)
    if face:
        return redirect(_build_url(face.pic_path))
    else:
        response.status = 404
        return "not found"

def _build_url(path):
    return urljoin(config.BASE_URL, path)

def _get_random(character):
    return Face.select().where(Face.character == character).order_by(
            peewee.fn.Random()).first()

app = bottle.default_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
