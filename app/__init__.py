from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import MySQLdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1007@127.0.0.1:3306/LawAssistant'
db = SQLAlchemy(app)

from api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)

