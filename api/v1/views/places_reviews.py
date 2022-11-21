#!/usr/bin/python3
""" This script provides views of Amenity """

from flask import abort, jsonify, request
from models import storage
from models.review import Review
from api.v1.views import app_views
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def review_by_place(place_id):
    data = storage.get(Place, place_id)
    if data is None:
        abort(404)
    return jsonify([review.to_dict() for review in data.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def show_review(review_id):
    res = storage.get(Review, review_id)
    if res is None:
        abort(404)
    return jsonify(res.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    reviews = storage.get(Review, review_id)
    if reviews is None:
        abort(404)
    reviews.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if not body.get('user_id'):
        return abort(400, {'message': 'Missing user_id'})
    body['place_id'] = place_id
    user = storage.get(User, body.get('user_id'))
    if user is None:
        abort(404)
    if not body.get('text'):
        abort(400, {'message': 'Missing text'})
    n_review = Review(**body)
    n_review.place_id = place_id
    n_review.save()
    return jsonify(n_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    body = request.get_json()
    if type(body) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id',
                     'place_id']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
