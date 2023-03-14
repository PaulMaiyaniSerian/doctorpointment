from . import MEDIA_ROOT, db, ALLOWED_HOSTS
from sqlalchemy.types import Boolean
from flask_login import UserMixin
import os

from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    # name = db.Column(db.String(200))
    is_system_user = db.Column(Boolean, default=False)
    is_doctor = db.Column(Boolean, default=False)
    # accounts = db.relationship('Account', backref='user', lazy=True)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000
    name = db.Column(db.String(10000), nullable=True)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000
    name = db.Column(db.String(10000), nullable=True)
    img = db.Column(db.String(10000), nullable=True)
    department  = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    is_top_2 = db.Column(Boolean, default=False)
    is_bottom_2 = db.Column(Boolean, default=False)
    is_top = db.Column(Boolean, default=False)
    


    def get_img(self):
        # print("/media/" + self.img)
        # return  "/static/media/" + self.img
        return os.path.join(MEDIA_ROOT, self.img)



class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000
    is_top = db.Column(Boolean, default=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)   # associated with the user
    img = db.Column(db.String(10000), nullable=True)
    department  = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='CASCADE'), nullable=False)
    profession = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bio = db.Column(db.String(10000), nullable=True)

    def get_img(self):
        # print("/media/" + self.img)
        # return  "/static/media/" + self.img
        return os.path.join(MEDIA_ROOT, self.img)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)   # associated with the user
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000

    patient = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    doctor = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'), nullable=False)
    service = db.Column(db.Integer, db.ForeignKey('service.id', ondelete='CASCADE'), nullable=False)
    appointment_date = db.Column(db.String(10000), nullable=True)
    appointment_time = db.Column(db.String(10000), nullable=True)

    status = db.Column(db.String(10000), nullable=True, default="pending")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy 000000000000
    from_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(10000), nullable=True, default="Empty")
