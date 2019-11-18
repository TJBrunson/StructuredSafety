from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    company = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64), index=True, unique=True)
    #next two lines conflict because they are both foreign keys to user table
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employees = db.relationship('User', backref='employee', lazy='dynamic')
    documents = db.relationship('Document', backref='documents', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.format(self.company_name)

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street_name_1 = db.Column(db.String(256))
    street_name_2 = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    postal_code = db.Column(db.Integer)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Address: {} {} \n {}, {} {}'.format(self.street_number, self.street_name, self.city, self.state, self.postal_code)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Document name: {}'.format(self.name)