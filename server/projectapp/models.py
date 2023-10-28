from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from projectapp.config import db, bcrypt
from sqlalchemy.orm import validates


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-reviews.user', )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    search_history = db.relationship('SearchHistory', backref='user')

    @validates('username')
    def validate_username(self, key,value):
         if len(value) < 3:
            raise ValueError('Username must be at least  3 characters long.')

    
    @validates('email')
    def validate_email(self, key, value):
        if not value.endswith('@gmail.com'):
             raise ValueError('Email must end with @gmail.com.')

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

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    search_date = db.Column(db.DateTime)
    


    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValueError('Search history name must be at least 3 characters long.')


"Authentication"
"Routes"
" session"
"Documentation"
"Request handling"
"shipping cost"