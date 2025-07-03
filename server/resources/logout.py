from flask import session
from flask_restful import Resource
from ..models import User
from ..config import db


class Logout(Resource):
    def delete(self):
        if session.get("user_id"):
            session["user_id"] = None
            return {}, 204
        return {"error": "Unauthorized"}, 401
