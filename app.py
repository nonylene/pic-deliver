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
        characters = config.CHARACTERS.keys()
        res = ', '.join(characters)
        return { "text" : res }

    if not text in config.CHARACTERS:
        return ""

    character = config.CHARACTERS[text]
    face = _get_random(text)

    if not face:
        return ""

    original_url = _build_url(face.pic_path)
    thumb_url = _build_url(face.thumb_path)

    return {
            "username": text,
            "icon_url": _build_static_url(character["img_path"]),
            "attachments": [
                {
                    "fallback": original_url,
                    "title": original_url,
                    "title_link": original_url,
                    "image_url": thumb_url,
                    "footer": "{0}: {1:.2f}%, {2}: {3:.2f}%".format(
                        face.character,
                        face.probability * 100,
                        face.character_1,
                        face.probability_1 * 100
                        ),
                    }
                ]
            }

@get("/character/<character>/random")
def character_random(character):
    face = _get_random(character)
    if face:
        return redirect(_build_url(face.pic_path))
    else:
        response.status = 404
        return "not found"

@get('/static/<filepath:path>', name="static")
def static(filepath):
    return bottle.static_file(filepath, root="static/")

def _build_url(path):
    return urljoin(config.BASE_PICTURE_URL, path)

def _build_static_url(path):
    return urljoin(urljoin(config.BASE_URL, "/static/"), path)

def _get_random(character):
    return Face.select().where(Face.character == character).order_by(
            peewee.fn.Random()).first()

app = bottle.default_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
