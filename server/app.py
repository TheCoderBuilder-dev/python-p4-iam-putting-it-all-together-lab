from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from server.models import db
from flask_migrate import Migrate


from server.resources.signup import Signup
from server.resources.login import Login
from server.resources.logout import Logout
from server.resources.check_session import CheckSession
from server.resources.recipes import RecipeIndex



app = Flask(__name__)
app.secret_key = 'hush'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
api = Api(app)

db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)


api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(RecipeIndex, '/recipes')
