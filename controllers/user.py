from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    fresh_jwt_required)

from flask_restful import Resource, reqparse
from formatters.formatter import format_user_to_json
from models.user import UserModel
from werkzeug.security import safe_str_cmp


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
    parser.add_argument('password',
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

    @fresh_jwt_required  # A fresh access token is required for the code block below to be run
    def post(self, email):

        if UserModel.find_by_email(email):
            return {"message": "A user already exists with the same email address, use a different one!"}, 400

        data = User.parser.parse_args()
        is_valid, error_message = UserModel.check_if_data_has_valid_format(email, **data)

        if is_valid:
            new_user = UserModel(email, **data)
            try:
                new_user.save_to_db()
                return format_user_to_json(new_user), 201
            except:
                return {"message": "An error occurred while creating the user!"}, 500
        else:
            return {"message": error_message}, 400

    @jwt_required
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
        user.password = data['password']
        user.phone = data['phone']
        user.gender = data['gender']

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while updating the user!"}, 500

        return format_user_to_json(user)

    def delete(self, email):
        user = UserModel.find_by_email(email)

        if not user:
            return {"message": "No such user associated with this email address!"}, 404

        user.delete_from_db()
        return {"message": "user deleted!"}


class UserList(Resource):
    @jwt_required  # Either the access token is fresh or not as long as it's valid - not expired or wrong
    def get(self):
        # Code below does the same thing using a lambda function instead of list comprehension  --- LIST COMPREHENSION
        return {'users': [format_user_to_json(user) for user in UserModel.find_all()]}
        # map() function returns a list of the results after applying the given function to     --- LAMBDA & MAP
        # each item of a given iterable (list, tuple etc.):
        # return {'users': list(map(lambda x: format_user_to_json(x), UserModel.query.all()))}


# With Flask_JWT_extended we have to create the login endpoint,
# in contrast with Flask_JWT creating the auth endpoint itself automatically
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        # get data from parser
        data = self.parser.parse_args()
        # find user in database
        user = UserModel.find_by_email(data["email"])
        # check password
        if user and safe_str_cmp(user.password, data["password"]):
            # now let's create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(identity=user.id)
            return{
                      "access_token": access_token,
                      "refresh_token": refresh_token
                  }, 201

        return {"message": "Invalid Credentials!"}, 401  # Unauthorized response code


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)
        return {"access_token": new_token}, 201










