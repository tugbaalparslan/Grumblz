from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse
from formatters.formatter import format_company_to_json
from models.company import CompanyModel


class Company(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('company_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # parser.add_argument('us_employer_id',
    #                     type=int,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    parser.add_argument('business_area',
                        type=str,
                        required=True,
                        choices=['finance', 'health care', 'education'], # this is case sensitive, so trying enum sqlalchemy instead!
                        help="This field must be either finance, health care, or education!"
                        )
    parser.add_argument('number_of_employees',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self, us_employer_id):

        if CompanyModel.find_by_us_employer_id(us_employer_id):
            return {"message": "A company already exists with the same employer ID, use a different one!"}, 400

        data = Company.parser.parse_args()
        is_valid, error_message = CompanyModel.check_if_data_has_valid_format(us_employer_id, **data)

        if is_valid:
            new_company = CompanyModel(us_employer_id, **data)
            try:
                format_company_to_json(new_company)
                new_company.save_to_db()
                return format_company_to_json(new_company), 201
            except:
                return {"message": "An error occurred while creating the company!"}, 500
        else:
            return {"message": error_message}, 400

    @jwt_required
    def get(self, us_employer_id):
        company = CompanyModel.find_by_us_employer_id(us_employer_id)

        if not company:
            return {"message": "No such company registered with this employer ID!"}, 404  # returns a tuple: (body, status code), (body:dictionary, status code: integer - default 200)
        else:
            return format_company_to_json(company)

    def put(self, us_employer_id):

        company = CompanyModel.find_by_us_employer_id(us_employer_id)

        if not company:
            return {"message": "No such company registered with this employer ID !"}, 404

        data = Company.parser.parse_args()
        company.company_name = data['company_name']
        company.business_area = data['business_area']
        company.number_of_employees = data['number_of_employees']
        company.phone = data['phone']
        company.address = data['address']

        try:
            company.save_to_db()
        except:
            return {"message": "An error occurred while updating the company info!"}, 500

        return format_company_to_json(company)

    @jwt_required
    def delete(self, us_employer_id):
        company = CompanyModel.find_by_us_employer_id(us_employer_id)

        if not company:
            return {"message": "No such company associated with this employer ID!"}, 404

        company.delete_from_db()
        return {"message": "company deleted!"}


class CompanyList(Resource):
    @jwt_optional  # use whenever you would like to send restricted amount of data if the user is not logged in
    def get(self):
        companies = CompanyModel.find_all()
        user_id = get_jwt_identity()
        if user_id:
            return {'companies': [format_company_to_json(x) for x in companies]}, 200
            # map() function returns a list of the results after applying the given function to
            # each item of a given iterable (list, tuple etc.)
            # return {'companies': list(map(lambda x: format_company_to_json(x), CompanyModel.find_all()))}
        else:
            return {"company names:": [company.company_name for company in companies],
                    "message": "Log in to get more details of the company list!"}, 200

