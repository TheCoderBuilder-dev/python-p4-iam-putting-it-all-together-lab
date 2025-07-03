from flask import request, session
from flask_restful import Resource
from ..models import Recipe, User
from ..config import db


class RecipeIndex(Resource):
    def get(self):
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return [r.to_dict() for r in user.recipes], 200

    def post(self):
        data = request.get_json()
        user_id = session.get("user_id")
        if not user_id:
            return {"error": "Unauthorized"}, 401

        try:
            recipe = Recipe(
                title=data.get("title"),
                instructions=data.get("instructions"),
                minutes_to_complete=data.get("minutes_to_complete"),
                user_id=user_id
            )

            db.session.add(recipe)
            db.session.commit()

            return recipe.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 422
