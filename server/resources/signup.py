from flask import request, session
from flask_restful import Resource
from server.models import User
from server.models import db


class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        image_url = data.get("image_url")
        bio = data.get("bio")

        if not username or not password:
            return {"error": "Username and password required"}, 422

        try:
            user = User(username=username, image_url=image_url, bio=bio)
            user.password_hash = password
            db.session.add(user)
            db.session.commit()
        except:
            return {"error": "Invalid signup data"}, 422

        session["user_id"] = user.id
        return user.to_dict(), 201
