from flask import jsonify, request, current_app, url_for
from . import api
from app.models import User
from app import db


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/user')
def get_user_by_username():
    username = request.args.get('username')
    user = User.query.filter(User.user_username == username).first_or_404()
    return jsonify(user.to_json())


@api.route('/user/')
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])


@api.route('/user/', methods=['POST'])
def add_user():
    json = request.json
    user_username = json.get('user_username')
    user_password = json.get('user_password')
    user_type = json.get('user_type')
    user_authentication = json.get('user_authentication', None)

    if user_username is None or user_username == '' \
            or user_password is None or user_password == '' \
            or user_type is None or user_type == '':
        return jsonify({'error': 'bad data'}), 400

    if User.query.filter(User.user_username == request.json.get('user_username')).all():
        return jsonify({'error': 'username existed'}), 400

    user = User(user_username, user_password, user_type, user_authentication)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201


@api.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    json = request.json
    user_password = json.get('user_password')
    user_type = json.get('user_type')
    user_authentication = json.get('user_authentication', None)

    if user_password == '' or user_type == '':
        return jsonify({'error': 'bad data'}), 400

    user = User.query.get_or_404(id)

    if user_password:
        user.user_password = user_password
    if user_type:
        user.user_type = user_type
    if user_authentication:
        user.user_authentication = user_authentication

    db.session.commit()
    return jsonify(user.to_json()), 201


@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    return jsonify(None), 204
