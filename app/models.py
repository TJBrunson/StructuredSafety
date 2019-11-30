from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    companies = db.relationship(
        "Company",
        primaryjoin=lambda : db.or_(
            User.id == db.foreign(Company.owner_id),
            User.id == db.foreign(Company.employee_id)
        ),
        viewonly=True,
    )

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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owners = db.relationship('User', foreign_keys=[owner_id])
    employees = db.relationship('User', foreign_keys=[employee_id])
    documents = db.relationship('Document')

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
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    company = db.Column(db.Integer, db.ForeignKey('company.id'))
    file_location = db.Column(db.String(256))

    def __repr__(self):
        return '<Document name: {}'.format(self.name)