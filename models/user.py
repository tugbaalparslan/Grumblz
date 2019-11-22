from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(11))
    gender = db.Column(db.String(10))

    def __init__(self, email, name, last_name, phone, gender):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.gender = gender

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
