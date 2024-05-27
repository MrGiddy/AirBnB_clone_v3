#!/usr/bin/python3
"""Defines base/common views for the HBNB-REST API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of objects by type"""
    classes = {
        "amenities": "Amenity", "cities": "City", "places": "Place",
        "reviews": "Review", "states": "State", "users": "User"}
    collection = {}
    for k, v in classes.items():
        type_count = {k: storage.count(v)}
        collection.update(type_count)
    return jsonify(collection)
