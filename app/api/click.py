from flask import jsonify, request, current_app, url_for
from . import api
from app.models import Click, Question
from app import db
from sqlalchemy import and_, func, desc
from app.util import json_data
from datetime import datetime, timedelta


@api.route('/click')
def get_click():
    questions = db.session.query(Question).join(Click, Click.question_id == Question.question_id)\
                     .filter(Click.click_date.between(datetime.now() - timedelta(days=7), datetime.now()))\
                     .group_by(Click.question_id)\
                     .order_by(desc(func.sum(Click.click_count))).limit(20)

    return json_data(1, [question.to_json() for question in questions])
