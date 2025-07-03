from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from server.config import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    __serialize_only__ = ['id', 'username', 'image_url', 'bio', 'recipes.id', 'recipes.title']
    serialize_rules = ('-recipes.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    # No backref here to avoid circular reference error
    recipes = db.relationship('Recipe', cascade='all, delete-orphan')

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes are write-only. Nice try though 😎")

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, value):
        if not value or value.strip() == '':
            raise ValueError('Username cannot be empty.')
        return value

    def __repr__(self):
        return f"<User {self.username}>"


class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    __serialize_only__ = ['id', 'title', 'instructions', 'minutes_to_complete', 'user.id', 'user.username', 'user.image_url']
    serialize_rules = ('-user.recipes',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Define the reverse relationship
    user = db.relationship('User')  # this creates recipe.user

    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == '':
            raise ValueError('Title is required.')
        return value

    @validates('instructions')
    def validate_instructions(self, key, value):
        if not value or len(value.strip()) < 50:
            raise ValueError('Instructions must be at least 50 characters long.')
        return value

    def __repr__(self):
        return f"<Recipe {self.title}>"
