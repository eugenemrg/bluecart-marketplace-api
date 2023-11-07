from flask import Flask
from flask_cors import CORS
from .extensions import api, db, migrate, bcrypt, jwt
from .routes import profile_ns, login_ns, search_ns, history_ns

def create_app():
    app = Flask(__name__)
    
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config["JWT_SECRET_KEY"] = "phase5JWTkey"
    
    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    api.add_namespace(profile_ns)
    api.add_namespace(login_ns)
    api.add_namespace(search_ns)
    api.add_namespace(history_ns)
    
    return app