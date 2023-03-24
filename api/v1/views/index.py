#!/usr/bin/python3
from flask import jsonify, make_response
from api.v1.views import app_views
import models
from models.service import Service
from models.city import City
from models.hospital import Hospital
from models.review import Review
from models.state import State
from models.user import User
@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    stat = {
            "services": models.storage.count(Service),
            "cities": models.storage.count(City),
            "hospitals": models.storage.count(Hospital),
            "reviews": models.storage.count(Review),
            "states": models.storage.count(State),
            "users": models.storage.count(User)
            }
    return jsonify(stat)
