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
            return {"message": "A user already exists with the same email address, use a different one!"}, 400

        data = User.parser.parse_args()
        is_valid, error_message = UserModel.check_if_data_has_valid_format(email, **data)

        if is_valid:
            new_user = UserModel(email, **data)
            try:
                new_user.save_to_db()
                return format_user_to_json(new_user)
            except:
                return {"message": "An error occurred while creating the user!"}, 500
        else:
            return {"message": error_message}, 400


    def get(self, email):
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "No such user registered with this email address"}, 404
        else:
            return format_user_to_json(user)

    def put(self, email):

        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "No such user registered with this email address!"}, 404

        data = User.parser.parse_args()
        user.name = data['name']
        user.last_name = data['last_name']
        user.phone = data['phone']
        user.gender = data['gender']

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while updating the user!"}, 500

        return format_user_to_json(user)








