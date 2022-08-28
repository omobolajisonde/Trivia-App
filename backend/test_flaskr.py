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
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'bolaji', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 1
        }

        self.incomplete_que = {
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
        }

        self.quiz_preset = {
            "previous_questions": [12,23],
            "quiz_category": {
                "type":"History",
                "id":4
            }
        }

        self.quiz_preset_reached = {
            "previous_questions": [12,23,24,25],
            "quiz_category": {
                "type":"History",
                "id":4
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def tests_get_categories(self):
        '''Tests successful GET categories'''
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['categories_']))

    def tests_404_failed_get_categories(self):
        '''Tests failed GET categories'''
        res = self.client().get("/categories/all")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found!')

    def tests_get_paginated_questions(self):
        '''Tests successful GET questions'''
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue((data['total_questions']))
        self.assertTrue(len(data['categories']))
        self.assertEqual((data['current_category']), None)

    def tests_404_requesting_invalid_page(self):
        '''Tests invalid GET questions page'''
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found!')

    def tests_delete_question(self):
        '''Tests successful DELETion of a question'''
        res = self.client().delete("/questions/18")
        data = json.loads(res.data)
        deleted_question = Question.query.get(18)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 18)
        self.assertEqual(deleted_question, None)

    def tests_422_failed_delete_question(self):
        '''Tests failed DELETE question'''
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable request!')

    def tests_create_question(self):
        '''Tests successful CREATion of a question'''
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        question = Question.query.get(data["created"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["created"], question.id)
        self.assertTrue(question)

    def tests_400_failed_create_question(self):
        '''Tests failed CREATE question'''
        res = self.client().post("/questions", json=self.incomplete_que)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'bad request!')

    def tests_search_questions(self):
        '''Tests search questions'''
        res = self.client().post("/questions/search", json={"searchTerm": "which"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertEqual((data['current_category']), None)
        self.assertTrue((data["total_questions"]))

    def tests_search_questions_without_results(self):
        '''Tests search questions with zero results'''
        res = self.client().post("/questions/search", json={"searchTerm": "hghjkl"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertFalse(len(data["questions"]))
        self.assertEqual((data['current_category']), None)
        self.assertFalse((data["total_questions"]))

    def tests_get_questions_by_category(self):
        '''Tests get questions by category'''
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        category = Category.query.get(1)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data['current_category'], category.id)
        self.assertTrue(data["total_questions"])

    def tests_404_category_not_found(self):
        '''Tests invalid GET category questions'''
        res = self.client().get("/categories/1000/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found!')

    def tests_set_quiz_questions(self):
        '''Tests successful setting of quiz questions'''
        res = self.client().post("/quizzes", json=self.quiz_preset)
        success = json.loads(res.data)["success"]
        data = json.loads(res.data)["question"]
        question = Question.query.get(data["id"])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)
        self.assertTrue(question)

    def tests_quiz_play_limit_reached(self):
        '''Tests when the quiz play limit has been reached'''
        res = self.client().post("/quizzes", json=self.quiz_preset_reached)
        success = json.loads(res.data)["success"]
        data = json.loads(res.data)["question"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(success, True)
        self.assertEqual(data, None)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
