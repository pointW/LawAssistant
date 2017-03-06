from flask import request
from . import api
from app.models import Collection
from app import db
from sqlalchemy import and_
from app.util import json_data


@api.route('/collection/<int:id>')
def get_collection(id):
    collection = Collection.query.get(id)
    if not collection:
        return json_data(0, 'collection not exist')
    else:
        return json_data(1, collection.to_json())


@api.route('/collection')
def get_collection_by_args():
    if not request.args:
        collections = Collection.query.all()
        if not collections:
            return json_data(0, 'no data')
        else:
            return json_data(1, [collection.to_json() for collection in collections])

    else:
        user_id = request.args.get('user_id')
        question_id = request.args.get('question_id')

        conditions = []
        if user_id:
            conditions.append(Collection.user_id == user_id)
        if question_id:
            conditions.append(Collection.question_id == question_id)

        if not conditions:
            return json_data(0, 'bad request')

        collections = Collection.query.filter(and_(*conditions)).all()
        if collections:
            return json_data(1, [collection.to_json() for collection in collections])
        else:
            return json_data(0, 'no data')


@api.route('/collection', methods=['POST'])
def add_collection():
    json = request.json
    user_id = json.get('user_id')
    question_id = json.get('question_id')

    if not user_id or not type(user_id) == int or not question_id or not type(question_id) == int:
        return json_data(0, 'bad request')

    conditions = [(Collection.user_id == user_id), (Collection.question_id == question_id)]
    if Collection.query.filter(and_(*conditions)).all():
        return json_data(0, 'collection existed')

    collection = Collection(user_id, question_id)
    db.session.add(collection)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return json_data(1, collection.to_json())


@api.route('/collection/<int:id>', methods=['DELETE'])
def delete_collection(id):
    collection = Collection.query.get(id)
    if not collection:
        return json_data(0, 'collection not exist')

    db.session.delete(collection)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)

    return json_data(1)

