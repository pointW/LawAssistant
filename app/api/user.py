from flask import jsonify, request, current_app, url_for
from . import api
from app.models import User
from app import db
from app.util import json_data


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'code': 0, 'msg': 'user not exist'})
    else:
        return jsonify({'code': 1, 'data': user.to_json()})


@api.route('/user')
def get_user_by_args():
    if not request.args:
        users = User.query.all()
        if not users:
            return jsonify({'code': 0, 'msg': 'no data'})
        else:
            return jsonify({'code': 1, 'data': [user.to_json() for user in users]})

    username = request.args.get('username')
    nickname = request.args.get('nickname')
    if username:
        user = User.query.filter(User.user_username == username).first()
        if user is None:
            return jsonify({'code': 0, 'msg': 'user not exist'})
        else:
            return jsonify({'code': 1, 'data': user.to_json()})
    elif nickname:
        users = User.query.filter(User.user_nickname == nickname).all()
        if users:
            return json_data(1, [user.to_json() for user in users])
        else:
            return json_data(0, 'no data')
    else:
        return json_data(0, 'bad request')


@api.route('/user', methods=['POST'])
def add_user():
    json = request.json
    user_username = json.get('user_username')
    user_password = json.get('user_password')
    user_type = json.get('user_type')
    user_authentication = json.get('user_authentication', None)
    user_nickname = json.get('user_nickname')

    if user_username is None or user_username == '' \
            or user_password is None or user_password == '' \
            or user_type is None or user_type == ''\
            or user_nickname is None or user_nickname == '':
        return jsonify({'code': 0, 'msg': 'bad request'})

    if User.query.filter(User.user_username == request.json.get('user_username')).all():
        return jsonify({'code': 0, 'msg': 'username existed'})

    user = User(user_username, user_password, user_type, user_authentication, user_nickname)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1, 'data': user.to_json()})


@api.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    json = request.json
    user_password = json.get('user_password')
    user_type = json.get('user_type')
    user_authentication = json.get('user_authentication', None)
    user_nickname = json.get('user_nickname')

    if user_password == '' or user_type == '':
        return jsonify({'code': 0, 'msg': 'bad request'})

    user = User.query.get(id)
    if user is None:
        return jsonify({'code': 0, 'msg': 'user not exist'})

    if user_password:
        user.user_password = user_password
    if user_type:
        user.user_type = user_type
    if user_authentication:
        user.user_authentication = user_authentication
    if user_nickname:
        user.user_nickname = user_nickname
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1, 'data': user.to_json()})


@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'code': 0, 'msg': 'user not exist'})

    db.session.delete(user)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1})
