#!/usr/bin/python3
'''module for the city routes'''
from flask import Blueprint, jsonify, request
from api.v1.views import City_view
import models
from models.state import State
from models.city import City


@City_view.route('/states/<state_id>/cities')
def GET_cities(state_id):
    state = models.storage.get(State, state_id)
    if (state):
        cities = state.cities
        return jsonify([city.to_dict() for city in cities])
    return jsonify({"Error": "State not found"}), 404


@City_view.route('/cities/<city_id>')
def GET_city(city_id):
    key = 'City.{}'. format(city_id)
    if (models.storage.all(City).get(key)):
        return jsonify(models.storage.all(City).get(key).to_dict())
    else:
        return jsonify({"Error": "not found"}), 404


@City_view.route('/cities/<city_id>', methods=['DELETE'])
def DELETE_city(city_id):
    key = 'City.{}'. format(city_id)
    city_o = models.storage.all(City)[key]

    if (city_o):
        models.storage.delete(city_o)
        models.storage.save()
        return jsonify({}), 200

    return jsonify({"Error": "not found"}), 404


@City_view.route('/states/<state_id>/cities', methods=['POST'])
def POST_city(state_id):
    state = models.storage.get(State, state_id)

    if (state):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'name' not in my_dict:
            return jsonify({'message': 'Missing name'}), 400
        city_o = City(**my_dict)
        city_o.state_id = state_id
        city_o.save()
        return jsonify(city_o.to_dict()), 201

    return jsonify({"Error": "State not found"}), 404


@City_view.route('/cities/<city_id>', methods=['PUT'])
def UPDATE_city(city_id):
    key = 'City.{}'. format(city_id)
    city_o = models.storage.all(City).get(key)

    if (city_o):
        req = request.get_json()
        if not req:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in req.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(city_o, k, v)
        city_o.save()
        return jsonify(city_o.to_dict()), 200

    return jsonify({"Error": "not found"}), 404
