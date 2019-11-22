from flask_restful import Resource, reqparse

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
        data = User.parser.parse_args()
        new_user = UserModel(email, **data)
        new_user.save_to_db()

    def get(self, email):
        pass

    def put(self, email):
        pass

