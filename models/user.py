from db import db


class UserModel(db.Model):  # UserModel objects are mapped to the DB rows - can be inserted/updated/.. etc
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # primary key is unique and indexed, auto-increments
    email = db.Column(db.String(80))  # this variable names must match the object variables -- self.email
    name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    phone = db.Column(db.String(11))
    gender = db.Column(db.String(10))

    def __init__(self, email, name, last_name, password, phone, gender):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.password = password
        self.phone = phone
        self.gender = gender

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def check_if_data_has_valid_format(cls, email, name, last_name, password, phone, gender):
        error_message = {}
        is_valid = True

        if not phone.isnumeric() or len(phone) != 10:
            is_valid = False
            error_message["phone"] = "Phone can be only 10 digits and all numeric!"

        return is_valid, error_message

    def save_to_db(self):  # used for update and insert - upsert
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
