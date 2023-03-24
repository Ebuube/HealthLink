#!/usr/bi/python3

from api.v1.views import Hospital_Service_view
from flask import jsonify, request
from models import storage
from models.hospital import Hospital
from models.service import Service


@Hospital_Service_view.route('/hospitals/<hospital_id>/services')
def GET_services(hospital_id):
    hospital = storage.get(Hospital, hospital_id)
    if not (hospital):
        return jsonify({"Error": "Hospital found"}), 404
    services = hospital.services
    if (services):
        return jsonify([o.to_dict() for o in services])
    return jsonify({"Error": "Service not found"}), 404


@Hospital_Service_view.route('/hospitals/<hospital_id>/services/<service_id>',
                             methods=['DELETE'])
def DELETE_service(hospital_id, service_id):
    hospital = storage.get(Hospital, hospital_id)
    service = storage.get(Service, service_id)
    if not hospital:
        return jsonify({"Error": "Hospital not found"}), 404
    if not service:
        return jsonify({"Error": "Service not found"}), 404
    for amen in hospital.services:
        if service_id == amen.id:
            hospital.services.remove(amen)
            storage.save()
            return jsonify({}), 200
    return jsonify({"Error": "Service not linked to State"}), 404


@Hospital_Service_view.route('/hospitals/<hospital_id>/services/<service_id>',
                          methods=['POST'])
def POST_service(hospital_id, service_id):
    hospital = storage.get(Hospital, hospital_id)
    service = storage.get(Service, service_id)
    if not hospital:
        return jsonify({"Error": "Hospital not found"}), 404
    if not service:
        return jsonify({"Error": "Service not found"}), 404
    for amen in hospital.services:
        if service_id == amen.id:
            return jsonify(amen.to_dict()), 200
    hospital.services.append(service)
    storage.save()
    return jsonify(service.to_dict()), 201
