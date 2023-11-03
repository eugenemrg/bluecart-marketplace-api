from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from .extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    search_history = db.relationship('SearchHistory', backref='user')

    @validates('name')
    def  validates_name(self, key, name):
        if  not name:
            raise ValueError('No name provided')
        return name
    
    @hybrid_property
    def password_hash(self):
        return self.password
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self.password = password_hash.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password, password.encode('utf-8'))


class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    search_date = db.Column(db.DateTime)