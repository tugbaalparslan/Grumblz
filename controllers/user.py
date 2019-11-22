from flask_restful import Resource, reqparse
from formatters.formatter import format_user_to_json
from models.user import UserModel


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self, email):

        if UserModel.find_by_email(email):
            return {"message": "A user already exists with the same email adress, use a different one!"}, 400

        data = User.parser.parse_args()
        is_valid, error_message = UserModel.check_if_data_has_valid_format(email, **data)

        if is_valid:
            new_user = UserModel(email, **data)
            new_user.save_to_db()
            return format_user_to_json(new_user)
        else:
            return {"message": error_message}, 400


    def get(self, email):
        user = UserModel.find_by_email(email)

        if user:
            return format_user_to_json(user)

        return {"message": "No such user!"}, 404


    def put(self, email):
        pass

