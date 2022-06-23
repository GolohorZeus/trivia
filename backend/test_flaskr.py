import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # setting up the app
        self.app = create_app()
        # setting up a test client
        # used to make hhtp request
        self.client = self.app.test_client
        # setting up database
        self.database_name = "trivia_test"
        # setting up database path for db connection
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # information new question
        self.new_question = {
            "question": "Test question",
            "answer": "Test answer",
            "category": 1,
            "difficulty": 1,
            "rating": 5
        }

        # information for quizze test
        self.quizze = {
            "previous_questions": [1],
            "quiz_category": {'id': 1, 'type': 'Science'}
        }

        # information for new category
        self.new_category = {
            "newCategory": "New category"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    ''' Test for categories end point '''

    # to get list of categories
    def test_get_categories(self):
        # making a request to the category end point
        res = self.client().get('/categories')
        # loading the data using json.loads
        # to load the response from the request
        data = json.loads(res.data)
        # use assert to check the response for the following
        # checking the status code 200 ok
        # status code is 200
        self.assertEqual(res.status_code, 200)
        # success is set to True
        # checking if success is true
        self.assertEqual(data['success'], True)
        # to check if some numbers of categories was returned
        self.assertTrue(len(data['categories']))
        # to check if a total of categories was returned
        self.assertTrue(data['total_categories'])

    # error test to get categories
    def test_404_sent_for_invaild_request_to_categories(self):
        # sendig a bad response
        res = self.client().get('/categories/1')
        # Loading the data using json.loads
        # to load the response from the request
        data = json.loads(res.data)

        # using assert to check the response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test to get questions base on categories
    def test_get_questions_base_on_categogies(self):
        # making the request
        res = self.client().get('/categories/1/questions')
        # loading the data
        data = json.loads(res.data)

        # using assert to response for the following
        # checking the status code 200 ok
        self.assertEqual(res.status_code, 200)
        # success is set to true
        self.assertEqual(data['success'], True)
        # to check if specific data was returned
        self.assertTrue(data['total_questions'])
        # to check if some questions was returned
        self.assertTrue(len(data['questions']))

    # test to get questions base on invalid categories
    def test_404_sent_requesting_questions_beyond_valid_categories(self):
        # making the request
        res = self.client().get('/categories/1000/questions')
        # loading the data using json.loads
        data = json.loads(res.data)

        # using assert to check for the following
        # status code is 400
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test to create new category
    def test_create_new_category(self):
        # making the request
        res = self.client().post('/categories', json=self.new_category)
        # loading the data using json.loads
        data = json.loads(res.data)

        # using assert to check the status
        # status code is 200
        self.assertEqual(res.status_code, 200)
        # success is set to True
        self.assertEqual(data["success"], True)

    # test to create category from the wrong route via post
    def test_400_for_category_creation_with_no_name(self):
        # making the request
        res = self.client().post('/categories', json={})
        # loading the data using json.loads
        data = json.loads(res.data)

        # status code is 405
        self.assertEqual(res.status_code, 400)
        # success is set to False
        self.assertEqual(data["success"], False)
        # message is correct
        self.assertEqual(data["message"], "bad request")

    ''' Test for questions end point '''
    # check for paginated questions

    def test_get_paginated_questions(self):
        # making a resquest to the questions end point
        res = self.client().get('/questions?page=1')
        # Loading the data using json.loads
        data = json.loads(res.data)

        # using assert to check for the following
        # status code is 200
        self.assertEqual(res.status_code, 200)
        # success is true
        self.assertEqual(data['success'], True)
        # There is a number for total questions
        self.assertTrue(data['total_questions'])
        # to check if some numbers of questions was returned
        self.assertTrue(len(data['questions']))

    # question invalid page error check
    def test_404_sent_requesting_beyond_valid_page_questions(self):
        # making the request
        res = self.client().get('/questiions?page=10000')
        # load the data using json.loads
        data = json.loads(res.data)

        # using assert to check the response
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test_delete_question
    # Delete a different question in each attempt
    # def test_delete_question(self):
    #     # specify the question id to be deleted
    #     question_id = 32
    #     # making the request
    #     res = self.client().delete('/questions/' + str(question_id))
    #     # storing the response data after the request has taken place
    #     data = json.loads(res.data)

    #     # querying the db for the specified question
    #     # question = Question.query.filter(Question.id == 1).one_or_none()

    #     # using assert to check the response for the following
    #     # status is 200 ok
    #     self.assertEqual(res.status_code, 200)
    #     # success is set True
    #     self.assertEqual(data['success'], True)
    #     # deleted the question with the specified id
    #     self.assertEqual(data['deleted_question'], question_id)

    # test to check if question exist
    def test_422_if_question_does_not_exist(self):
        # making the request
        # (which does not exist)
        # trying to get a question that does not exist
        res = self.client().delete('/questions/50000')
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check for the following
        self.assertEqual(res.status_code, 422)
        # success is set to false
        self.assertEqual(data['success'], False)
        # message is correct
        self.assertEqual(data['message'], 'unprocessable')

    # test to create new question
    # def test_create_new_question(self):
        # making the request
        res = self.client().post("/questions", json=self.new_question)
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response
        # status code is 200 ok
        self.assertEqual(res.status_code, 200)
        # success is set to true
        self.assertEqual(data['success'], True)

    # test to create a new question a wrong route
    def test_405_if_question_creation_not_allowed(self):
        # making the request
        res = self.client().post("/questions/10000", json=self.new_question)
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response data
        self.assertEqual(res.status_code, 405)
        # success is set to false
        self.assertEqual(data['success'], False)
        # message is correct
        self.assertEqual(data['message'], 'method not allowed')

    # test to search for a question
    def test_get_question_search_with_results(self):
        # making the request
        res = self.client().post("/questions", json={'searchTerm': 'movie'})
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response
        # status code is 200
        self.assertEqual(res.status_code, 200)
        # success is set to true
        self.assertEqual(data['success'], True)
        # totalQuestions is returned
        self.assertTrue(data['totalQuestions'])
        # questions were returned
        self.assertTrue(data['questions'])

    # test to search for question that dont exits
    def test_get_question_search_without_results(self):
        # making the request
        res = self.client().post(
            "/questions", json={'searchTerm': 'Golohor Zeus'})
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response
        self.assertEqual(res.status_code, 200)
        # success is set to True
        self.assertEqual(data['success'], True)
        # total questions is 0
        self.assertEqual(data['totalQuestions'], 0)
        # length of questions is 0
        self.assertEqual(len(data['questions']), 0)

    '''Test for quizzes'''
    # test to get quizze

    def test_get_quizze(self):
        # making the request
        res = self.client().post('/quizzes', json=self.quizze)
        # load the data using json.loads
        data = json.loads(res.data)

        # using assert to check the response
        # checking the status code 200 ok
        self.assertEqual(res.status_code, 200)
        # success is set to true
        self.assertEqual(data['success'], True)
        # a question was returned
        self.assertTrue(data['question'])
        # previous question was returned
        self.assertTrue(len(data['previousQuestions']))

    # test to make sure same question is not returned for quizze
    def test_check_quezze_not_repeated(self):
        # making the request
        res = self.client().post('/quizzes',
                                 json={
                                     'previous_questions': [22],
                                     'quiz_category': {
                                         'id': 1,
                                         'type': 'Science'
                                     }
                                 })
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response
        # status code is 200
        self.assertEqual(res.status_code, 200)
        # success is set to true
        self.assertEqual(data["success"], True)
        # to check that the returned question
        # as a category equal to the specified category
        self.assertEqual(int(data['question']['category']), 1)
        # to check that the same quizze is not returned twice
        self.assertNotEqual(int(data['question']['id']), 22)

    # test to get quizze via wrong method
    def test_405_if_quizze_request_not_allowed(self):
        # making the request
        res = self.client().get('/quizzes',
                                json={
                                    'previous_questions': [22],
                                    'quiz_category': {
                                        'id': 1,
                                        'type': 'Science'
                                    }
                                }
                                )
        # storing the respose data after the request as taken place
        data = json.loads(res.data)

        # using assert to check the response
        # status code is 405
        self.assertEqual(res.status_code, 405)
        # success is set to False
        self.assertEqual(data["success"], False)
        # message is correct
        self.assertEqual(data["message"], "method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
