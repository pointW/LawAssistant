from flask import jsonify, request, current_app, url_for
from . import api
from app.models import Answer
from app import db
from sqlalchemy import and_
from app.util import json_data


@api.route('/answer/<int:id>')
def get_answer(id):
    answer = Answer.query.get(id)
    if answer is None:
        return json_data(0, 'answer not exist')
    else:
        return json_data(1, answer.to_json())


@api.route('/answer')
def get_answer_by_args():
    if not request.args:
        answers = Answer.query.all()
        if not answers:
            return json_data(0, 'no data')
        else:
            return json_data(1, [answer.to_json() for answer in answers])

    else:
        question_id = request.args.get('question_id')
        user_id = request.args.get('user_id')
        answer_draft = request.args.get('answer_draft', 0)

        conditions = []
        if question_id:
            conditions.append(Answer.question_id == question_id)
        if user_id:
            conditions.append(Answer.user_id == user_id)
        conditions.append(Answer.answer_draft == answer_draft)

        if not conditions:
            return json_data(0, 'bad request')

        answers = Answer.query.filter(and_(*conditions)).all()
        if answers:
            return json_data(1, [answer.to_json() for answer in answers])
        else:
            return json_data(0, 'no data')


@api.route('/answer', methods=['POST'])
def add_answer():
    json = request.json
    question_id = json.get('question_id')
    user_id = json.get('user_id')
    answer_detail = json.get('answer_detail')
    answer_draft = json.get('answer_draft', 0)

    if not user_id or not type(user_id) == int or not question_id or not type(question_id) == int:
        return json_data(0, 'bad request')

    answer = Answer(question_id, user_id, answer_detail, answer_draft)
    db.session.add(answer)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return json_data(1, answer.to_json())


@api.route('/answer/<int:id>', methods=['PUT'])
def update_answer(id):
    json = request.json
    answer_detail = json.get('answer_detail')
    answer_draft = json.get('answer_draft', 0)

    answer = Answer.query.get(id)
    if answer is None:
        return json_data(0, 'answer not exist')

    answer.answer_draft = answer_draft
    if answer_detail:
        answer.answer_detail = answer_detail
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return json_data(1, answer.to_json())


@api.route('/answer/<int:id>', methods=['DELETE'])
def delete_answer(id):
    answer = Answer.query.get(id)
    if answer is None:
        return json_data(0, 'answer not exist')

    db.session.delete(answer)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)

    return json_data(1)

