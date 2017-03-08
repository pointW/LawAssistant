from flask import jsonify, request, current_app, url_for
from . import api
from app.models import Type, Question
from app import db
from sqlalchemy import and_
from app.util import json_data


@api.route('/type/<int:id>')
def get_type(id):
    t = Type.query.get(id)
    if not t:
        return json_data(0, 'type not exist')
    else:
        return json_data(1, t.to_json())


@api.route('/type')
def get_type_by_args():
    if not request.args:
        types = Type.query.all()
        if not types:
            return json_data(0, 'no data')
        else:
            return json_data(1, [t.to_json() for t in types])

    else:
        return json_data(0, 'bad request')


