from db import db
# import enum
#
#
# class BusinessChoices(enum.Enum):
#     finance = 'finance'
#     health_care = 'health care'
#     education = 'education'


class CompanyModel(db.Model):  # CompanyModel objects are mapped to the DB rows - can be inserted/updated/.. etc
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    us_employer_id = db.Column(db.String(50))
    company_name = db.Column(db.String(200))
    # business_area = db.Column(db.Enum(BusinessChoices), nullable=False)  # ******* this should be enum *******
    business_area = db.Column(db.String(50), nullable=False)
    number_of_employees = db.Column(db.Integer)
    phone = db.Column(db.String(11))
    address = db.Column(db.String(250))

    def __init__(self, us_employer_id, company_name, business_area, number_of_employees, phone, address):

        self.us_employer_id = us_employer_id
        self.company_name = company_name
        self.business_area = business_area
        self.number_of_employees = number_of_employees
        self.phone = phone
        self.address = address

    @classmethod
    def find_by_us_employer_id(cls, us_employer_id):
        return cls.query.filter_by(us_employer_id=us_employer_id).first()

    @classmethod
    def check_if_data_has_valid_format(cls, us_employer_id, company_name, business_area, number_of_employees, phone, address):
        error_message = {}
        is_valid = True

        if not phone.isnumeric() or len(phone) != 10:
            is_valid = False
            error_message["phone"] = "Phone can be only 10 digits and all numeric!"

        return is_valid, error_message

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
