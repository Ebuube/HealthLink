#!/usr/bin/python3
from flask import Blueprint, jsonify, make_response, request
from api.v1.views import Hospital_view
import models
from models.city import City
from models.hospital import Hospital


@Hospital_view.route('/cities/<city_id>/hospitals')
def GET_hospitals(city_id):
    ob = models.storage.get(City, city_id)
    if (ob):
        o_l = ob.hospitals
        return jsonify([o.to_dict() for o in o_l])
    return make_response(jsonify({"Error": "City not found"}), 404)

@Hospital_view.route('/hospitals/<city_id>')
def GET_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)
    if (models.storage.all(Hospital).get(key)):
        return jsonify(models.storage.all(Hospital).get(key).to_dict())
    else:
        return make_response(jsonify({"Error": "not found"}), 404)

@Hospital_view.route('/hospitals/<city_id>', methods=['DELETE'])
def DELETE_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)
    ob = models.storage.all(Hospital)[key]
    models.storage.delete(ob)
    models.storage.save()
    models.storage.reload()
    return jsonify({}), 200

@Hospital_view.route('/cities/<city_id>/hospitals', methods=['POST'])
def POST_hospital(city_id):
    ob = models.storage.get(City, city_id)

    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'name' not in my_dict:
            return jsonify({'message': 'Missing name'}), 400
        ob = Hospital(**my_dict)
        ob.city_id = city_id
        ob.save()
        models.storage.reload()
        return jsonify(ob.to_dict()), 201
    return make_response(jsonify({"Error": "City not found"}), 404)

@Hospital_view.route('/hospitals/<city_id>', methods=['PUT'])
def PUT_hospital(city_id):
    key = 'Hospital.{}'. format(city_id)
    ob = models.storage.all(Hospital).get(key)
    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in my_dict.items():
            if k not in ['id', 'created_at',
                         'updated_at', 'user_id', 'city_id']:
                setattr(ob, k, v)
        ob.save()
        return jsonify(ob.to_dict()), 200
    return make_response(jsonify({"Error": "not found"}), 404)
