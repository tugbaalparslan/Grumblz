from datetime import timedelta
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Controllers are imported to:
# 1. create tables (table details are stored in Models)
# Controllers already import models. So no need to re-import.
# 2. To add resource endpoints to api
from controllers.company import Company, CompanyList
from controllers.user import User, UserList

app = Flask(__name__)

# Tell SQLAlchemy where and which DB to read. SQLAlchemy can read sqlite, postgreSQL, mySQL, Oracle, etc
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datagrumblz.db'
# Turns off Flask-SQLALchemy's change tracking feature for better performance,
# still SQLAlchemy's main library has its own tracking features on.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key gotta be long, secure and secret. not to be exposed in production.
# So, I created an environment variable called "CUSTOM_APP_SECRET_KEY". Api reads the value from there.
# app.secret_key is used to sign the token to make sure it won't be tampered. if tampered JWT Extension will detect it.
app.secret_key = os.environ.get("CUSTOM_APP_SECRET_KEY")
# app.secret_key = 'tugba'  # ABOVE CODE implement later -- today is the day!
api = Api(app)


@app.before_first_request  # whatever the first request comes, code below will run
def create_tables():
    db.create_all()  # SQLAlchemy creates tables, import from resources ultimately from import models


# changing the default /auth endpoint to /login. if we don't specify anything, it will be /auth
app.config['JWT_AUTH_URL_RULE'] = '/login'
# changing the default "username" parameter to "email". email will be sent in requests's body -- update postman!
app.config['JWT_AUTH_USERNAME_KEY'] = 'user_email'
# config JWT to expire within X minutes, default is 5 minutes = 300 sc
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=300)

# IMPORTANT!: JWT Extension automatically creates /auth endpoint with the code below. Test w Postman /auth endpoint
# with the /auth endpoint, username+password is sent. JWT automatically sends this request auth method under security.py
jwt = JWT(app, authenticate, identity)

api.add_resource(User, '/user/<string:email>')
api.add_resource(UserList, '/users/')
api.add_resource(Company, '/company/<string:us_employer_id>')
api.add_resource(CompanyList, '/companies/')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)

