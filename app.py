from datetime import timedelta  # using to set the expiration period of Jason Web Token
import os  # using to access the environment variables -  eg. CUSTOM_APP_SECRET_KEY

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Controllers are imported to:
# 1. create tables (table details are stored in Models)
# Controllers already import models. So no need to re-import.
# 2. To add resource endpoints to api
from controllers.company import Company, CompanyList
from controllers.user import User, UserList, UserLogin, TokenRefresh

app = Flask(__name__)

# Tell SQLAlchemy where and which DB to read. SQLAlchemy can read sqlite, postgreSQL, mySQL, Oracle, etc
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datagrumblz.db'
# Turns off Flask-SQLALchemy's change tracking feature for better performance,
# still SQLAlchemy's main library has its own tracking features on.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Turn on the propogate exceptions - when flask throws exceptions it will be propagated to the user so user can have
# a better understanding of the exception's details, otherwise it will be masked such as 500 - internal server error.
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key gotta be long, secure and secret. not to be exposed in production.
# So, I created an environment variable called "CUSTOM_APP_SECRET_KEY". Api reads the value from there.
# app.secret_key is used to sign the token to make sure it won't be tampered. if tampered JWT Extension will detect it.
app.secret_key = os.environ.get("CUSTOM_APP_SECRET_KEY")
# stored the secret_key in environment variable, so when the code is published, secret key won't be disclosed
# app.secret_key = 'tugba'
api = Api(app)


@app.before_first_request  # whatever the first request comes, code below will run
def create_tables():
    db.create_all()  # SQLAlchemy creates tables, import from resources ultimately from import models


# config JWT access token to expire within X minutes, default is 5 minutes = 300 sc
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=300)
# config JWT refresh token to expire within X minutes, default is 5 minutes = 300 sc
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=300)


# Link JWT with our app
jwt = JWTManager(app)


# This is the custom message we will send when the token expires
@jwt.expired_token_loader
def expired_token_callback():
    return {"error": "token_expired", "description": "The token has expired."}, 401

api.add_resource(User, '/user/<string:email>')
api.add_resource(UserList, '/users/')
api.add_resource(Company, '/company/<string:us_employer_id>')
api.add_resource(CompanyList, '/companies/')
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)

