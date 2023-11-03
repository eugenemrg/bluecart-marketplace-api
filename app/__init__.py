from flask import Flask
from .extensions import api, db, migrate, bcrypt
from .routes import profile_ns, login_ns, history_ns

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
    api.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    api.add_namespace(profile_ns)
    api.add_namespace(login_ns)
    api.add_namespace(history_ns)
    
    return app