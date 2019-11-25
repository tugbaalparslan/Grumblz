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
                return format_company_to_json(new_company)
            except:
                return {"message": "An error occurred while creating the user!"}, 500
        else:
            return {"message": error_message}, 400

    def get(self, us_employer_id):
        company = CompanyModel.find_by_us_employer_id(us_employer_id)

        if not company:
            return {"message": "No such company registered with this employer ID!"}, 404
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

    #
    def delete(self, us_employer_id):
        company = CompanyModel.find_by_us_employer_id(us_employer_id)

        if not company:
            return {"message": "No such company associated with this employer ID!"}, 404

        company.delete_from_db()
        return {"message": "company deleted!"}



