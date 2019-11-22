from flask import Flask
from flask_restful import Api

from controllers.user import User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datagrumblz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
#app.secret_key = 'tugba'  # will implement later
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()  # SQLAlchemy creates tables, import from resources ultimately from import models


# jwt = JWT(app, authenticate, identity)  # IMPORTANT!: JW Extension automatically creates /auth resource with this line of code

api.add_resource(User, '/user/<string:email>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001, debug=True)

