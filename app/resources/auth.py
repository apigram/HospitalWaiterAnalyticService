from flask_restful import Resource, fields
from flask import jsonify, g
from app import auth
from app.models import User

user_fields = {
    "username": fields.String,
    "patient": fields.Url('patient'),
    "token": fields.String
}