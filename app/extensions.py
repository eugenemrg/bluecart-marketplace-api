from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt

api = Api()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()