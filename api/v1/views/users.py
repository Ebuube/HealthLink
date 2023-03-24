#!/usr/bin/python3

from flask import jsonify, request
from api.v1.views import User_view
from models import storage
from models.user import User


@User_view.route('/users')
def GET_users():
    return jsonify([o.to_dict() for o in storage.all(User).values()])


@User_view.route('/users/<user_id>')
def GET_user(user_id):
    ob = storage.get(User, user_id)

    if (ob):
        return jsonify(ob.to_dict())

    return jsonify({"Error": "Not found"}), 404


@User_view.route('/users/<user_id>', methods=['DELETE'])
def DELETE_user(user_id):
    ob = storage.get(User, user_id)

    if (ob):
        storage.delete(ob)
        storage.save()
        return jsonify({})

    return jsonify({"Error": "Not found"}), 404


@User_view.route('/users', methods=['POST'])
def POST_user():
    o_d = request.get_json()

    if not o_d:
        return jsonify({"Error": "Not a JSON"}), 400
    if 'email' not in o_d:
        return jsonify({"Error": "missing email"}), 400
    if 'password' not in o_d:
        return jsonify({"Error": "Missing password"}), 400

    ob = User(**o_d)
    ob.save()
    return jsonify(ob.to_dict())


@User_view.route('/users/<user_id>', methods=['PUT'])
def PUT_user(user_id):
    o_d = request.get_json()

    if not o_d:
        return jsonify({"Error": "Not a JSON"}), 400
    ob = storage.get(User, user_id)
    if (ob):
        for k, v in o_d.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(ob, k, v)
        storage.save()
        return jsonify(ob.to_dict()), 200
    return jsonify({"Error": "Not found"}), 404
