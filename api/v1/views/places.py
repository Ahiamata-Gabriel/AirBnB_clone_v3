#!/usr/bin/python3
""" This script provides views of Amenity """

from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def place_by_city(city_id):
    data = storage.get(City, city_id)
    if data is None:
        abort(404)
    return jsonify([place.to_dict() for place in data.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_places(place_id):
    res = storage.get(Place, place_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    places = storage.get(Place, place_id)
    if places is None:
        abort(404)
    places.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if not body.get('user_id'):
        return abort(400, {'message': 'Missing user_id'})
    user = storage.get(User, body.get('user_id'))
    if user is None:
        abort(404)
    if not body.get('name'):
        abort(400, {'message': 'Missing name'})
    n_place = Place(**body)
    n_place.city_id = city_id
    n_place.save()
    return jsonify(n_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id',
                     'city_id']:
            setattr(user, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
