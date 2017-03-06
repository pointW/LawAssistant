from flask import Blueprint

api = Blueprint('api', __name__)

from . import user, question, answer, collection, comment

