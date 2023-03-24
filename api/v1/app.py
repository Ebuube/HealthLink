#!/usr/bin/python3
'''module contains my app'''
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from os import getenv
import models
from api.v1.views import app_views
from api.v1.views import State_view
from api.v1.views import City_view
from api.v1.views import Service_view
from api.v1.views import User_view
from api.v1.views import Hospital_view
from api.v1.views import Review_view
from api.v1.views import Hospital_Service_view

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/api/v1')
app.register_blueprint(State_view, url_prefix='/api/v1')
app.register_blueprint(City_view, url_prefix='/api/v1')
app.register_blueprint(Service_view, url_prefix='/api/v1')
app.register_blueprint(User_view, url_prefix='/api/v1')
app.register_blueprint(Hospital_view, url_prefix='/api/v1')
app.register_blueprint(Review_view, url_prefix='/api/v1')
app.register_blueprint(Hospital_Service_view, url_prefix='/api/v1')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(exception):
    models.storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=getenv('HLINK_API_HOST', '0.0.0.0'),
            port=getenv('HLINK_API_PORT', 5000), threaded=True)
