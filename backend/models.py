import os
from sqlalchemy import (
    Column,
    String,
    Integer,
    create_engine
)
from flask_sqlalchemy import SQLAlchemy
import json
# Adding migration to our application
from flask_migrate import Migrate

database_name = 'trivia'
database_path = "postgresql://{}:{}@{}/{}".format(
    "student", "student", "localhost:5432", database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    migrate = Migrate(app, db)
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Question

"""


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)
    rating = Column(Integer)

    # for debugging
    def __repr__(self):
        return f'<Question id: {self.id},\
             question: {self.question},\
             answer: {self.answer},\
             category: {self.category},\
             difficulty: {self.difficulty}, rating: {self.rating}>'

    def __init__(self, question, answer, category, difficulty, rating):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty,
            'rating': self.rating
        }


"""
Category

"""


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    # for debuggin
    def __repr__(self):
        return f'<Category id: {self.id}, type: {self.type}>'

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
