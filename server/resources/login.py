from flask import request, session, jsonify
from flask_restful import Resource
from ..models import User
from ..config import db


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Missing JSON body"}, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"error": "Username and password required"}, 400

        user = User.query.filter_by(username=username).first()

        if not user or not user.authenticate(password):
            return {"error": "Unauthorized"}, 401

        session["user_id"] = user.id

        return jsonify({
            "id": user.id,
            "username": user.username,
            "image_url": user.image_url,
            "bio": user.bio
        })
