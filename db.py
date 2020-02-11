from flask_sqlalchemy import SQLAlchemy

# Creating a SQLAlchemy object here, we are gonna map our other objects in the app into database rows with this object.
# In the model files, we are going to import this object
# SQLAlchemy is an ORM (object-relation mapper) meaning mapping the DB rows to the class objects
db = SQLAlchemy()