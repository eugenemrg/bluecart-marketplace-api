from flask_sqlalchemy  import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import validates
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,ValidationError
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)

db = SQLAlchemy()
bcrypt = Bcrypt(app)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-reviews.user', )
    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    search_history = db.relationship('User')

    @validates('username')
    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError('Username must be at least  3 characters long.')

    
    @validates('email')
    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise ValidationError('Email must end with @example.com.')

    @hybrid_property
    def password_hash(self):
        return self.password
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self.password = password_hash.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password, password.encode('utf-8'))


class SearchHistory(db.Model, SerializerMixin):
    __tablename__ = 'search_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    search_date = Column(DateTime)

    User = db.relationship('User' ,back_populate= 'SearchHistory')

    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('Search history name must be at least 3 characters long.')

