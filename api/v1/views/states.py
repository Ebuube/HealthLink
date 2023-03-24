#!/usr/bin/python3
from flask import Blueprint, jsonify, make_response, request
from api.v1.views import State_view
import models
from models.state import State


@State_view.route('/states')
def states():
    o_d = models.storage.all(State)
    return jsonify([o.to_dict() for o in o_d.values()])

@State_view.route('/states/<state_id>')
def state_id(state_id):
    key = 'State.{}'. format(state_id)
    if (models.storage.all(State).get(key)):
        return jsonify(models.storage.all(State).get(key).to_dict())
    else:
        return make_response(jsonify({"Error": "not found"}), 404)

@State_view.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    key = 'State.{}'. format(state_id)
    ob = models.storage.all(State)[key]
    models.storage.delete(ob)
    models.storage.save()
    models.storage.reload()
    return jsonify({}), 200

@State_view.route('/states', methods=['POST'])
def make():
    my_dict = request.get_json()

    if not my_dict:
        return jsonify({'message': 'Not a JSON'}), 400
    if 'name' not in my_dict:
        return jsonify({'message': 'Missing name'}), 400
    ob = State(**my_dict)
    ob.save()
    models.storage.reload()
    return jsonify(ob.to_dict()), 201

@State_view.route('/states/<state_id>', methods=['PUT'])
def up_date(state_id):
    key = 'State.{}'. format(state_id)
    ob = models.storage.all(State).get(key)
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
