from datetime import datetime
from . import db
from marshmallow import Schema, fields
from exceptions import ValidationError


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(45), nullable=False, unique=True)
    user_password = db.Column(db.String(45), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    user_authentication = db.Column(db.String(45))
    user_nickname = db.Column(db.String(45))

    def __init__(self, user_username, user_password, user_type, user_authentication, user_nickname):
        self.user_username = user_username
        self.user_password = user_password
        self.user_type = user_type
        self.user_authentication = user_authentication
        self.user_nickname = user_nickname

    def to_json(self):
        json_user = {
            'user_id': self.user_id,
            'user_username': self.user_username,
            'user_password': self.user_password,
            'user_type': self.user_type,
            'user_authentication': self.user_authentication,
            'user_nickname': self.user_nickname
        }
        return json_user

    # @staticmethod
    # def from_json(json_post):
    #     user_username = json_post.get('user_username')
    #     user_password = json_post.get('user_password')
    #     user_type = json_post.get('user_type')
    #     user_authentication = json_post.get('user_authentication', None)
    #     if user_username is None or user_username == ''\
    #         or user_password is None or user_password == ''\
    #             or user_type is None or user_type == '':
    #         raise ValidationError('data error')
    #     return User(user_username, user_password, user_type, user_authentication)


# class UserSchema(Schema):
#     user_id = fields.Int(dump_only=True)
#     user_username = fields.Str()
#     user_password = fields.Str()
#     user_type = fields.Int()
#     user_authentication = fields.Str()
#
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_detail = db.Column(db.String)
    question_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.ForeignKey('user.user_id'))
    question_draft = db.Column(db.Boolean)

    def __init__(self, question_detail, user_id, question_draft):
        self.question_detail = question_detail
        # self.question_time = question_time
        self.user_id = user_id
        self.question_draft = question_draft

    def to_json(self):
        json_question = {
            'question_id': self.question_id,
            'question_detail': self.question_detail,
            'question_time': self.question_time,
            'user_id': self.user_id,
            'question_draft': self.question_draft
        }
        return json_question


class Answer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.ForeignKey('question.question_id'))
    user_id = db.Column(db.ForeignKey('user.user_id'))
    answer_detail = db.Column(db.String)
    answer_time = db.Column(db.DateTime, default=datetime.now)
    answer_draft = db.Column(db.Boolean)

    def __init__(self, question_id, user_id, answer_detail, answer_draft):
        self.question_id = question_id
        self.user_id = user_id
        self.answer_detail = answer_detail
        self.answer_draft = answer_draft

    def to_json(self):
        json_answer = {
            'answer_id': self.answer_id,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'answer_detail': self.answer_detail,
            'answer_time': self.answer_time,
            'answer_draft': self.answer_draft
        }
        return json_answer


class Collection(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.user_id'))
    question_id = db.Column(db.ForeignKey('question.question_id'))

    def __init__(self, user_id, question_id):
        self.user_id = user_id
        self.question_id = question_id

    def to_json(self):
        json_collection = {
            'collection_id': self.collection_id,
            'user_id': self.user_id,
            'question_id': self.question_id
        }
        return json_collection


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_detail = db.Column(db.String)
    comment_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.ForeignKey('user.user_id'))
    question_id = db.Column(db.ForeignKey('question.question_id'))

    def __init__(self, comment_detail, user_id, question_id):
        self.comment_detail = comment_detail
        self.user_id = user_id
        self.question_id = question_id

    def to_json(self):
        json_comment = {
            'comment_id': self.comment_id,
            'comment_detail': self.comment_detail,
            'comment_time': self.comment_time,
            'user_id': self.user_id,
            'question_id': self.question_id
        }
        return json_comment


class Click(db.Model):
    click_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.ForeignKey('question.question_id'))
    click_date = db.Column(db.Date, default=datetime.now().date())
    click_count = db.Column(db.Integer, default=1)

    def __init__(self, question_id):
        self.question_id = question_id


question_type = db.Table('question_type',
                         db.Column('question_id', db.Integer, db.ForeignKey('question.question_id')),
                         db.Column('type_id', db.Integer, db.ForeignKey('type.type_id'))
                         )


class Type(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String, nullable=False, unique=True)

    questions = db.relationship('Question', secondary=question_type, backref=db.backref('types', lazy='dynamic'))

    # def __init__(self, type_name):
    #     self.type_name = type_name

    def to_json(self):
        json_type = {
            'type_id': self.type_id,
            'type_name': self.type_name,
            'questions': [question.to_json() for question in self.questions]
        }
        return json_type









