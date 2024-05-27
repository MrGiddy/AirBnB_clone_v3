#!/usr/bin/python3
"""Defines views for the HBNB-REST API"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns the OK status of the API"""
    return jsonify({"status": "OK"})
