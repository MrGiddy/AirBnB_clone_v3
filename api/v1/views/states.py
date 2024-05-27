#!/usr/bin/python3
"""Defines the view for State objects"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """Retrieves a State abject or all State objects from storage"""
    if state_id:
        the_state = storage.get(State, state_id)
        if not the_state:
            abort(404)
        return jsonify(the_state.to_dict())
    else:
        all_states = [obj.to_dict() for obj in storage.all(State).values()]
        return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object of the given id from storage"""
    the_state = storage.get(State, state_id)
    if not the_state:
        abort(404)
    storage.delete(the_state)
    storage.save()
    return {}, 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a State object and saves it in storage"""
    data_dict = request.get_json()

    if not data_dict:
        abort(400, "Not a JSON")
    if "name" not in data_dict.keys():
        abort(400, "Missing name")

    new_state = State(**data_dict)
    storage.new(new_state)
    storage.save()

    return storage.get(State, new_state.id).to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates the information of a State object"""
    the_state = storage.get(State, state_id)
    if not the_state:
        abort(404)
    data_dict = request.get_json()
    if not data_dict:
        abort(400, description="Not a JSON")

    for k, v in data_dict.items():
        if k not in ('id', 'created_at', 'updated_at'):
            setattr(the_state, k, v)

    storage.all().update(**(the_state.__dict__))
    storage.save()

    return storage.get(State, the_state.id).to_dict(), 200
