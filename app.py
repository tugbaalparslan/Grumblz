from flask import Flask
from flask_restful import Api

from controllers.company import Company, CompanyList
from controllers.user import User, UserList

app = Flask(__name__)

# Tell SQLAlchemy where and which DB to read. SQLAlchemy can read sqlite, postgreSQL, mySQL, Oracle, etc
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datagrumblz.db'
# Turns off Flask-SQLALchemy's change tracking feature for better performance,
# still SQLAlchemy's main library has its own tracking features on.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.secret_key = 'tugba'  # will implement later *************!!!!!!*******************
api = Api(app)


@app.before_first_request  # whatever the first request comes, code below will run
def create_tables():
    db.create_all()  # SQLAlchemy creates tables, import from resources ultimately from import models

# IMPORTANT!: JW Extension automatically creates /auth resource with this line of code
# jwt = JWT(app, authenticate, identity)


api.add_resource(User, '/user/<string:email>')
api.add_resource(UserList, '/users/')
api.add_resource(Company, '/company/<string:us_employer_id>')
api.add_resource(CompanyList, '/companies/')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)

