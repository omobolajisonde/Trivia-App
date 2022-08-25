from distutils.log import error
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, close_db, rollback_db, Question, Category

QUESTIONS_PER_PAGE = 10



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    CORS setup. Allowed '*' for origins.
    """
    CORS(app, resources={"*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, POST, PATCH, PUT, DELETE, OPTIONS")
        return response

    def paginate_questions(request,questions):
        page = request.args.get("page",1,int)
        start = (page * QUESTIONS_PER_PAGE) - QUESTIONS_PER_PAGE
        stop = start + QUESTIONS_PER_PAGE

        formatted_questions =  [que.format() for que in questions[start:stop]]

        return formatted_questions

    """
    GETs all avaliable categories
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = [category.format() for category in categories]
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type # Populating the dict with category rows
            print(categories_dict)
            return jsonify({
                "success": True,
                "categories": categories_dict,
                "categories_": formatted_categories
            })
        except:
            abort(500) # Internal Server Error

    """
    GETs paginated questions
    """
    
    @app.route("/questions", methods=["GET"])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        selected_questions = paginate_questions(request,questions)

        categories = Category.query.order_by(Category.id).all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type # Populating the dict with category rows

        return jsonify({
            "questions": selected_questions,
            "total_questions": len(questions),
            "categories": categories_dict,
            "current_category": categories_dict[1]
        })
        
        


    """
    DELETEs a question
    """

    @app.route("/questions/<int:que_id>", methods=["DELETE"])
    def delete_question(que_id):
        error = None
        try:
            question = Question.query.get(que_id)
            if (question is None):
                abort(404)
            else:
                question.delete()
        except:
            error = True
            rollback_db()
        finally:
            close_db()
        if error:
            abort(422) # Unprocessable
        else:
            return jsonify({
                "success": True,
                "deleted": que_id
            })


    """
    CREATEs a new question given the required parameters
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        question_data = request.get_json()
        error = None
        body = {}
        try:
            new_question = Question(question_data["question"],question_data["answer"],question_data["category"],question_data["difficulty"])
            new_question.insert()
            body["id"] = new_question.id
        except:
            error = True
            rollback_db()
        finally:
            close_db()
        if error:
            abort(500)
        else:
            return jsonify({
                "success": True,
                "created": body.get("id")
            })

    """
    GETs paginated questions based on search query
    """

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        search_query = request.get_json().get("searchTerm")
        print(search_query)
        questions = Question.query.filter(Question.question.ilike("%{}%".format(search_query))).all()
        selected_questions = paginate_questions(request,questions)

        return jsonify({
            "success": True,
            "questions": selected_questions,
            "total_questions": len(questions),
            "current_category": "Science"  # TODO
        })

    """
    GETs paginated questions by category
    """

    @app.route("/categories/<cat_id>/questions", methods=["GET"])
    def get_questions_by_category(cat_id):
        questions = Question.query.filter_by(category = cat_id).all()
        selected_questions = paginate_questions(request,questions)

        return jsonify({
            "success": True,
            "questions": selected_questions,
            "total_questions": len(questions),
            "current_category": "Science"  # TODO
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/quizzes", methods=["POST"])
    def set_quiz_questions():
        question = {}
        error = None
        try:
            previous_questions = request.get_json().get("previous_questions")
            quiz_category = request.get_json().get("quiz_category")
            questions = None
            if quiz_category["type"] == "All":
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=quiz_category["id"]).all()
            random_num = random.randint(0,(len(questions)-1))
            random_question = questions[random_num]
            is_unique_que = False
            while not is_unique_que:
                count = previous_questions.count(random_question.id)
                if count:
                    random_num = random.randint(0,(len(questions)-1))
                    random_question = questions[random_num]
                else:
                    break
            question = {
                    "id": random_question.id,
                    "question": random_question.question,
                    "answer": random_question.answer,
                    "difficulty": random_question.difficulty,
                    "category": random_question.category
                }
        except:
            error = True
        if error:
            abort(500)
        else:
             return jsonify({
                "question": question
            })


           

    """
    Error Handling
    """
    app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found!"
        }), 404

    app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed!"
        }), 404

    app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable request!"
        }), 422

    app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error!"
        })

    return app
