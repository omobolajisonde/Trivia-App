# TRIVIA APP 🎯

## Description

Trivia app is a web-based trivia gaming application, where users can not only play trivia games but also expand their general knowledge in various fields like `history`, `geography`, `science` etc.

Built as a project in the [Udacity's Full Stack web developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Tech Stack
### 1. Backend Dependencies
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** as an ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-CORS** to handle cross origin request from our frontend server

### 2. Frontend Dependencies
* The frontend of this project is built with **React js** and some third party packages like **react router**.

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── backend
  │   ├── flaskr
  │   │   ├── __init__.py
  │   ├── models.py
  │   ├── requirements.txt *** The dependencies to be installed with "pip install -r requirements.txt"
  │   ├── test_flaskr.py *** contains code for testing the api endpoints.
  │   └── trivia.psql *** contains instructions for populating the database.
  ├── frontend
  │   ├── public
  │   │   ├── index.html
  └── ├── src
      │   ├── components
      │   ├── stylesheets
      │   ├── App.js
      │   ├── App.test.js
      │   ├── index.js
      └──  package.json
  ```

## Getting Started

### Prerequisites & Installation
To be able to get this application up and running, ensure to have [python3](https://www.python.org/downloads/) and [node](https://nodejs.org/en/download/) installed on your device.

### Development Setup (Backend)
1. **Download the project locally by forking this repo and then clone or just clone directly via:**
```
git clone https://github.com/omobolajisonde/Trivia-App.git 
```
2. **Set up the Database**
   with Postgres running, create a trivia database
``` bash
createdb trivia
```
3. **Populate the database using the `trivia.psql` file provided. From the backend folder in terminal run:**
``` bash
psql trivia < trivia.psql
```

4. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```

5. **Install the backend dependencies** from the backend folder in terminal run:
```
pip install -r requirements.txt
```

6. **Run the development server:**
```
export FLASK_APP=flaskr
export FLASK_DEBUG=true # enables debug mode
python flaskr
```
7. **At this point, your server should be up and running** at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

### Development Setup (frontend)
1. **This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:**
``` bash
npm install
```
2. **Starting the frontend in devlopment mode** from the frontend folder run:
``` bash
npm start
```
3. **At this point, the frontend should be up and running** at [http://127.0.0.1:3000/](http://127.0.0.1:3000/) or [http://localhost:3000](http://localhost:3000)

## Testing
In order to run tests navigate to the backend folder and run the following commands:
``` bash
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```
>**Note** - All tests are in the `test_flaskr.py` file.

# API REFERENCE
### Getting Started
- Base URL: The app is currently not deployed and can only be tested out if setup on your local machine. The backend runs on `http://127.0.0.1:5000` and connected as proxy to the frontend.

- Authentication: No authentication or any sort of unique keys for this version of the application

### Error Handling
- Format: All responses to requests including failed ones are returned in JSON (JavaScript Object Notation) format.
```
{
    "success": false,
    "error": code,
    "message": "error message"
}
```

Potential error types that could be encountered on failed request
- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints
`GET '/categories'`
- Returns: two categories objects (with different format of the categories), `categories` and `categories_` whose values are a dictionary of the categories (key:id and value:category string) and a list of category dictionaries respectively and a success value.
- Request parameter: None
- Sample
```bash
curl http://127.0.0.1:5000/categories
```
- Response (JSON)
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "categories_": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

---

`GET '/questions?page={integer}'`

- Fetches a paginated set of questions, a total number of questions, a success state, all categories and current category id.
- Request Arguments (optional): `page` - integer (default `page` is `1`)
- Returns: A list of 10 questions (based on the current page), total questions, categories object (including all categories), and current category id.
- Sample
```bash
curl http://127.0.0.1:5000/questions?page=1
```
- Response (JSON)
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
  ],
  "success": true,
  "total_questions": 27
}
```

---

`GET '/categories/{id}/questions'`

- Fetches questions for a cateogry based on the id in the URL
- Request Arguments: `id` - integer
- Request Arguments (optional): `page` - integer (default `page` is `1`)
- Returns: A list of questions (paginated) for the specified category, total questions, current category id and a success value
- Sample
```bash
curl http://127.0.0.1:5000/categories/1/questions
```
- Response (JSON)
```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Jupiter",
      "category": 1,
      "difficulty": 2,
      "id": 32,
      "question": "What is the largest planet in the solar system?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```
---

`DELETE '/questions/{id}'`

- Deletes a specific question based on the id in the url
- Request Arguments: `id` - integer
- Returns: A success value and the id of the deleted question
- Sample
```bash
curl -X DELETE http://127.0.0.1:5000/questions/5
```
- Response (JSON)
```json
{
  "deleted": 5,
  "success": true
}
```
---
`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "What is the name of the longest river in Africa?",
  "answer": "The Nile River",
  "difficulty": 4,
  "category": 3
}
```
- Returns: A success value and the id of the created question
- Sample
```bash
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"What is the name of the longest river in Africa?", "answer":"The Nile River", "difficulty":"4", "category":"3"}'
```
- Response (JSON)
```json
{
  "created": 36,
  "success": true
}
```

---

`POST '/questions/search'`

- Sends a post request in order to query for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "substring of the question the user is looking for"
}
```

- Returns: a list of questions, a number of total questions that met the search term, a success value and the current category id
- Sample
```bash
curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"won"}'
```
- Response (JSON)
```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
---

`POST '/quizzes'`

- Sends a post request in order to get the next quiz question.
- Request Body:

```json
{
  "previous_questions": [9,12],
  "quiz_category": {
    "id": 4,
    "type": "History"
  }
}
```

- Returns: a new question object or a question value of none (when the category has no more unique question or when play limit has been reached) and a success value.
- Sample
```bash
curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [9, 12],"quiz_category": {"id": 4,"type": "History"}}'
```
- Response (JSON)
```json
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```
**OR**
```json
{
  "question": null,
  "success": true
}
```
## Deployment N/A

## Authors
[Sonde Omobolaji](https://github.com/omobolajisonde) 

## Acknowledgements 
The awesome team at Udacity and my dear [Coach Caryn McCarthy](https://www.linkedin.com/in/carynmccarthy)

