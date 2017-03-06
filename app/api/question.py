from flask import jsonify, request, current_app, url_for
from . import api
from app.models import Question
from app import db
from sqlalchemy import and_
from app.util import json_data


@api.route('/question/<int:id>')
def get_question(id):
    question = Question.query.get(id)
    if question is None:
        return jsonify({'code': 0, 'msg': 'question not exist'})
    else:
        return jsonify({'code': 1, 'data': question.to_json()})


@api.route('/question')
def get_question_by_args():
    if not request.args:
        questions = Question.query.all()
        if not questions:
            return jsonify({'code': 0, 'msg': 'no data'})
        else:
            return jsonify({'code': 1, 'data': [question.to_json() for question in questions]})

    user_id = request.args.get('user_id')
    keyword = request.args.get('keyword')
    question_draft = request.args.get('draft', 0)

    conditions = []
    if keyword:
        conditions.append(Question.question_detail.like('%'+keyword+'%'))
    if user_id:
        conditions.append(Question.user_id == user_id)
    conditions.append(Question.question_draft == question_draft)

    if not conditions:
        return json_data(0, 'bad request')

    questions = Question.query.filter(and_(*conditions)).all()
    if questions:
        return json_data(1, [question.to_json() for question in questions])
    else:
        return json_data(0, 'no data')

    # if keyword:
    #     questions = Question.query.filter(and_(Question.question_detail.like('%'+keyword+'%')),
    #                                       (Question.question_draft == 0)).all()
    #     if questions:
    #         return jsonify({'code': 1, 'data': [question.to_json() for question in questions]})
    #     else:
    #         return jsonify({'code': 0, 'msg': 'no data'})
    #
    # elif user_id and question_draft:
    #     questions = Question.query.filter(and_(Question.user_id == user_id),
    #                                       (Question.question_draft == question_draft)).all()
    #     if questions:
    #         return jsonify({'code': 1, 'data': [question.to_json() for question in questions]})
    #     else:
    #         return jsonify({'code': 0, 'msg': 'no data'})
    #
    # elif user_id and not question_draft:
    #     questions = Question.query.filter(Question.user_id == user_id).all()
    #     if questions:
    #         return jsonify({'code': 1, 'data': [question.to_json() for question in questions]})
    #     else:
    #         return jsonify({'code': 0, 'msg': 'no data'})
    #
    # else:
    #     return json_data(0, 'bad request')


@api.route('/question', methods=['POST'])
def add_question():
    json = request.json
    question_detail = json.get('question_detail')
    user_id = json.get('user_id')
    question_draft = json.get('question_draft', 0)

    if user_id is None or not type(user_id) == int:
        return jsonify({'code': 0, 'msg': 'bad request'})

    question = Question(question_detail, user_id, question_draft)
    db.session.add(question)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1, 'data': question.to_json()})


@api.route('/question/<int:id>', methods=['PUT'])
def update_question(id):
    json = request.json
    question_detail = json.get('question_detail')
    question_draft = json.get('question_draft', 0)

    question = Question.query.get(id)
    if question is None:
        return jsonify({'code': 0, 'msg': 'question not exist'})

    question.question_draft = question_draft
    if question_detail:
        question.question_detail = question_detail

    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1, 'data': question.to_json()})


@api.route('/question/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if question is None:
        return json_data(0, 'question not exist')

    db.session.delete(question)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return jsonify({'code': 1})



