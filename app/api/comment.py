from flask import request
from . import api
from app.models import Comment
from app import db
from sqlalchemy import and_
from app.util import json_data


@api.route('/comment/<int:id>')
def get_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return json_data(0, 'comment not exist')
    else:
        return json_data(1, comment.to_json())


@api.route('/comment')
def get_comment_by_args():
    if not request.args:
        comments = Comment.query.all()
        if not comments:
            return json_data(0, 'no data')
        else:
            return json_data(1, [comment.to_json() for comment in comments])

    else:
        question_id = request.args.get('question_id')
        user_id = request.args.get('user_id')

        conditions = []
        if question_id:
            conditions.append(Comment.question_id == question_id)
        if user_id:
            conditions.append(Comment.user_id == user_id)

        if not conditions:
            return json_data(0, 'bad request')

        comments = Comment.query.filter(and_(*conditions)).all()
        if comments:
            return json_data(1, [comment.to_json() for comment in comments])
        else:
            return json_data(0, 'no data')


@api.route('/comment', methods=['POST'])
def add_comment():
    json = request.json
    user_id = json.get('user_id')
    question_id = json.get('question_id')
    comment_detail = json.get('comment_detail')

    if not user_id or not type(user_id) == int or not question_id or not type(question_id) == int:
        return json_data(0, 'bad request')

    comment = Comment(comment_detail, user_id, question_id)
    db.session.add(comment)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)
    return json_data(1, comment.to_json())


@api.route('/comment/<int:id>', methods=['PUT'])
def update_comment(id):
    json = request.json
    comment_detail = json.get('comment_detail')

    comment = Comment.query.get(id)
    if not comment:
        return json_data(0, 'comment not exist')

    comment.comment_detail = comment_detail
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)

    return json_data(1, comment.to_json())


@api.route('/comment/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return json_data(0, 'comment not exist')

    db.session.delete(comment)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return json_data(0, e.message)

    return json_data(1)
