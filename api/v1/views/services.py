#!/usr/bin/python3
from flask import Blueprint, jsonify, make_response, request
from api.v1.views import Service_view
import models
from models.service import Service


@Service_view.route('/services')
def services():
    o_d = models.storage.all(Service)
    return jsonify([o.to_dict() for o in o_d.values()])

@Service_view.route('/services/<service_id>')
def service_id(service_id):
    key = 'Service.{}'. format(service_id)
    if (models.storage.all(Service).get(key)):
        return jsonify(models.storage.all(Service).get(key).to_dict())
    else:
        return make_response(jsonify({"Error": "not found"}), 404)

@Service_view.route('/services/<service_id>', methods=['DELETE'])
def delete(service_id):
    ob = models.storage.get(Service, service_id)
    if (ob):
        models.storage.delete(ob)
        models.storage.save()
        return jsonify({}), 200
    return make_response(jsonify({"Error": "not found"}), 404)

@Service_view.route('/services', methods=['POST'])
def make():
    my_dict = request.get_json()

    if not my_dict:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in my_dict:
        return jsonify({'message': 'Missing name'}), 400
    ob = Service(**my_dict)
    ob.save()
    models.storage.reload()
    return jsonify(ob.to_dict()), 201

@Service_view.route('/services/<service_id>', methods=['PUT'])
def up_date(service_id):
    key = 'Service.{}'. format(service_id)
    ob = models.storage.all(Service).get(key)
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
