#!/usr/bin/python3
from flask import Blueprint, jsonify, make_response, request
from api.v1.views import City_view
import models
from models.state import State
from models.city import City


@City_view.route('/states/<state_id>/cities')
def cities(state_id):
    ob = models.storage.get(State, state_id)
    if (ob):
        o_l = ob.cities
        return jsonify([o.to_dict() for o in o_l])
    return make_response(jsonify({"Error": "State not found"}), 404)

@City_view.route('/cities/<city_id>')
def city_id(city_id):
    key = 'City.{}'. format(city_id)
    if (models.storage.all(City).get(key)):
        return jsonify(models.storage.all(City).get(key).to_dict())
    else:
        return make_response(jsonify({"Error": "not found"}), 404)

@City_view.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    key = 'City.{}'. format(city_id)
    ob = models.storage.all(City)[key]
    models.storage.delete(ob)
    models.storage.save()
    models.storage.reload()
    return jsonify({}), 200

@City_view.route('/states/<state_id>/cities', methods=['POST'])
def make_city(state_id):
    ob = models.storage.get(State, state_id)

    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'name' not in my_dict:
            return jsonify({'message': 'Missing name'}), 400
        ob = City(**my_dict)
        ob.state_id = state_id
        ob.save()
        models.storage.reload()
        return jsonify(ob.to_dict()), 201
    return make_response(jsonify({"Error": "State not found"}), 404)

@City_view.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    key = 'City.{}'. format(city_id)
    ob = models.storage.all(City).get(key)
    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in my_dict.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(ob, k, v)
        ob.save()
        return jsonify(ob.to_dict()), 200
    return make_response(jsonify({"Error": "not found"}), 404)
