from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# from flask_mail import Mail
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__, static_url_path="")
cors = CORS(app, resources={r"/biservice/*": {"origins": "*"}})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# mail = Mail(app)
auth = HTTPTokenAuth(scheme='Bearer')

from app import routes
# Register RESTful web service routes