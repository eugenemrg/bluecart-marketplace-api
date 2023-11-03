from flask_sqlalchemy import SQLAlchemy
from projectapp import  app
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


api = Api()
db = SQLAlchemy

    
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.json.compact = False

#db = SQLAlchemy()
migrate = Migrate(app, db)
#db.init_app(app)

bcrypt = Bcrypt(app)
