#!/usr/bin/python3
"""Defines the view for City objects"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    if state_id:
        the_state = storage.get(State, state_id)
        if the_state is None:
            abort(404)
        return jsonify([city.to_dict() for city in the_state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    if city_id:
        the_city = storage.get(City, city_id)
        if the_city is None:
            abort(404)
        return jsonify(the_city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City object"""
    if state_id:
        # Check that the state_id is linked to a State object
        the_state = storage.get(State, state_id)
        if the_state is None:
            abort(404)

        # Transform request body to a dictionary
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")

        # Check that data has name of the city to create
        if "name" not in data.keys():
            abort(400, "Missing name")

        # Create the new city and save it to storage
        new_city = City(**data)
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()

        # Retrieve the created City from storage and return it
        return storage.get(City, new_city.id).to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    if city_id:
        # Check that the city_id is linked to a City object
        the_city = storage.get(City, city_id)
        if city_id is None:
            abort(404)

        # Transform the request body to a dictionary
        # and check that the request body is a valid JSON
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")

        # Update the City object with all k, v pairs of data
        for k, v in data.items():
            if k not in ('id', 'created_at', 'updated_at'):
                setattr(the_city, k, v)

        # Ovewrite the City object with the modified version
        storage.new(the_city)
        storage.save()

        # Return the City object with the status code 200
        return jsonify(storage.get(City, the_city.id).to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object of id city_id"""
    if city_id:
        # If the city_id is not linked to any City object
        the_city = storage.get(City, city_id)
        if the_city is None:
            abort(404)
        # If the city_id is linked to a City object
        storage.delete(the_city)
        storage.save()
        return jsonify({}), 200
