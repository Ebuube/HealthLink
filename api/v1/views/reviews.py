#!/usr/bin/python3
from flask import Blueprint, jsonify, make_response, request
from api.v1.views import Review_view
import models
from models.hospital import Hospital
from models.review import Review


@Review_view.route('/hospitals/<hospital_id>/reviews')
def GET_reviews(hospital_id):
    ob = models.storage.get(Hospital, hospital_id)
    if (ob):
        o_l = ob.reviews
        return jsonify([o.to_dict() for o in o_l])
    return make_response(jsonify({"Error": "Hospital not found"}), 404)

@Review_view.route('/reviews/<review_id>')
def GET_review(review_id):
    key = 'Review.{}'. format(review_id)
    if (models.storage.all(Review).get(key)):
        return jsonify(models.storage.all(Review).get(key).to_dict())
    else:
        return make_response(jsonify({"Error": "not found"}), 404)

@Review_view.route('/reviews/<review_id>', methods=['DELETE'])
def DELETE_review(review_id):
    key = 'Review.{}'. format(review_id)
    ob = models.storage.all(Review)[key]
    models.storage.delete(ob)
    models.storage.save()

    return jsonify({}), 200

@Review_view.route('/hospitals/<hospital_id>/reviews', methods=['POST'])
def POST_review(hospital_id):
    ob = models.storage.get(Hospital, hospital_id)

    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        if 'text' not in my_dict:
            return jsonify({'message': 'Missing text'}), 400
        if 'user_id' not in my_dict:
            return jsonify({'message': 'Missing user_id'}), 400
        r_o = Review(**my_dict)
        r_o.hospital_id = hospital_id
        r_o.save()
        models.storage.reload()
        return jsonify(r_o.to_dict()), 201
    return make_response(jsonify({"Error": "Hospital not found"}), 404)

@Review_view.route('/reviews/<review_id>', methods=['PUT'])
def PUT_review(review_id):
    key = 'Review.{}'. format(review_id)
    ob = models.storage.all(Review).get(key)
    if (ob):
        my_dict = request.get_json()
        if not my_dict:
            return jsonify({'message': 'Not a JSON'}), 400
        for k, v in my_dict.items():
            if k not in ['id', 'created_at',
                         'updated_at', 'user_id', 'hospital_id']:
                setattr(ob, k, v)
        ob.save()
        return jsonify(ob.to_dict()), 200
    return make_response(jsonify({"Error": "not found"}), 404)
