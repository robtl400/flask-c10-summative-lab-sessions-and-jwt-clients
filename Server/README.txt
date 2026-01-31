Flask JWT Authentication API
============================

A secure REST API with JWT-based authentication and a notes resource. Users can only access their own notes.


Installation
------------

1. Install dependencies:
   pipenv install

2. Enter the virtual environment:
   pipenv shell

3. Initialize the database:
   flask db init

4. Run migrations:
   flask db migrate -m "initial migration"
   flask db upgrade

5. Seed the database (optional):
   python seed.py

   This creates test users:
   - username: testuser, password: password123
   - username: otheruser, password: password123


Running the Server
------------------

flask run -p 5555

Or:

python app.py

The server runs on http://localhost:5555


API Endpoints
-------------

Authentication:

POST /signup
  - Registers a new user
  - Body: { "username": "string", "password": "string", "password_confirmation": "string" }
  - Returns: { "token": "jwt_string", "user": { "id": 1, "username": "string" } }

POST /login
  - Authenticates an existing user
  - Body: { "username": "string", "password": "string" }
  - Returns: { "token": "jwt_string", "user": { "id": 1, "username": "string" } }

GET /me
  - Returns the current authenticated user
  - Requires: Authorization header with Bearer token
  - Returns: { "id": 1, "username": "string" }


Notes (all require Authorization header with Bearer token):

GET /notes
  - Returns paginated list of the current user's notes
  - Query params: page (default 1), per_page (default 10)
  - Returns: { "notes": [...], "page": 1, "per_page": 10, "total": 15, "pages": 2 }

GET /notes/<id>
  - Returns a specific note owned by the current user
  - Returns: { "id": 1, "title": "string", "content": "string", "created_at": "iso_date", "updated_at": "iso_date", "user_id": 1 }

POST /notes
  - Creates a new note for the current user
  - Body: { "title": "string", "content": "string" }
  - Returns: the created note object

PATCH /notes/<id>
  - Updates a note owned by the current user
  - Body: { "title": "string", "content": "string" } (both optional)
  - Returns: the updated note object

DELETE /notes/<id>
  - Deletes a note owned by the current user
  - Returns: { "message": "Note deleted successfully" }


Dependencies (Pipfile)
----------------------

flask = "2.2.2"
flask-sqlalchemy = "3.0.3"
Werkzeug = "2.2.2"
marshmallow = "3.20.1"
faker = "15.3.2"
flask-migrate = "4.0.0"
flask-restful = "0.3.9"
importlib-metadata = "6.0.0"
importlib-resources = "5.10.0"
flask-bcrypt = "1.0.1"
flask-jwt-extended = "*"

Dev dependencies:
pytest = "7.2.0"
