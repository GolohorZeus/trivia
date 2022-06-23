from operator import truediv
import os
from sre_parse import CATEGORIES
from unicodedata import category
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from sqlalchemy.sql.expression import func

from models import (
    setup_db,
    Question,
    Category,
    db
)

QUESTIONS_PER_PAGE = 10

# to paginate categories


def paginate_questions(request, selection):
    # pagination page setUp
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE  # 0
    end = start + QUESTIONS_PER_PAGE  # 10

    # formatting the results
    question = [question.format() for question in selection]
    current_questions = question[start:end]

    return current_questions

# formatted categories


def format_categories(categories):
    # getting categories from db
    categories = [category.format() for category in categories]
    # var object to store categories
    data = {}
    # looping through available categories and storing them
    for category in categories:
        data[category['id']] = category['type']
    return data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS Headers set up
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # to get all available categories
    @app.route('/categories', methods=['GET'])
    def retrieve_all_available_categories():
        # to get categories and then ordering them by their ids
        selection = Category.query.order_by(Category.id).all()
        category = format_categories(selection)

        # to check for errors
        if len(selection) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'categories': category,
                'total_categories': Category.query.count()
            }
        )

    # to create a new category
    @app.route('/categories', methods=['POST'])
    def create_category():
        # to get data from the request
        body = request.get_json()
        # getting and storing the form data
        newCategory = body.get("newCategory", None)
        error = False

        # to check if the request is empty or not
        if newCategory is None:
            abort(400)

        try:
            error = False
            # creating the new category
            category = Category(type=newCategory)
            category.insert()
        except Exception:
            error = True
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            if not error:
                return jsonify(
                    {
                        'success': True,
                    }
                )

    # to get paginated questions
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        # getting all questions from the db
        selection = Question.query.order_by(Question.id).all()
        # paginationg questions
        current_questions = paginate_questions(request, selection)

        # to check if questions are available
        if len(current_questions) == 0:
            abort(404)
        # formatting categories
        categories = format_categories(Category.query.all())
        # returning a json
        return jsonify({
            "success": True,
            'questions': current_questions,
            'total_questions': Question.query.count(),
            'categories': categories,
            'currentCategory': None
        })

    # to delete a question base on id

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            # to check if a valid question was returned
            if question is None:
                abort(404)

            # to delete the question from the db
            question.delete()

            # returning the deleted question id for UI update
            return jsonify(
                {
                    'success': True,
                    'deleted_question': question_id
                }
            )

        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        # to get data from the request
        body = request.get_json()
        # getting and storing the form data
        question = body.get("question", None)
        answer = body.get("answer", None)
        difficulty = body.get("difficulty", None)
        rating = body.get("rating", None)
        category = body.get("category", None)
        # store search data if it exist in the request
        search = body.get("searchTerm", None)

        error = False
        #  to check if the request is for a search or for a question creation
        if search:
            selection = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(search))
            )
            current_questions = paginate_questions(request, selection)
            return jsonify(
                {
                    'success': True,
                    'questions': current_questions,
                    'totalQuestions': selection.count(),
                    'currentCategory': None
                }
            )
        else:
            try:
                error = False
                # creating a new question
                question = Question(
                    question=question,
                    answer=answer,
                    category=int(category),
                    difficulty=int(difficulty),
                    rating=int(rating)
                )
                question.insert()
            except Exception:
                error = True
                db.session.rollback()
                print(sys.exc_info())
                abort(422)
            finally:
                if not error:
                    return jsonify(
                        {
                            'success': True,
                        }
                    )

    # to get question base on category

    @ app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_category_questions(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, selection)
        # to check for errors
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': Question.query.count(),
                'current_category': Category.query
                .filter_by(id=category_id).first()
                .type
            }
        )

    # to get quizzes
    @app.route('/quizzes', methods=['POST'])
    def retrieve_quizzes():
        # To store data from the request
        body = request.get_json()
        try:
            # to get quizze by ccategory
            # all category quizze
            if body['quiz_category']['id'] == 0:
                # get random question from the database
                question = Question.query.filter(
                    Question.id.notin_(body['previous_questions']))\
                    .order_by(func.random()).first()
            else:
                # getting random question base on specified category
                question = Question.query.filter(
                    Question.id.notin_(body['previous_questions']))\
                    .filter_by(category=body['quiz_category']['id'])\
                    .order_by(func.random()).first()

            return jsonify(
                {
                    'success': True,
                    'previousQuestions': body['previous_questions'],
                    'question': question.format()
                }
            )
        except Exception:
            abort(422)

    """
    Error handlers for all expected errors
    including 404 and 422.
    """
    @ app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @ app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @ app.errorhandler(400)
    def bad_request(error):
        return (jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400)

    @ app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )
    return app
