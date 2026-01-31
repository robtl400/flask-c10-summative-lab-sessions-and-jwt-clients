from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User, Note

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    password_confirmation = data.get('password_confirmation')

    errors = []

    if not username:
        errors.append('Username is required')
    if not password:
        errors.append('Password is required')
    if password != password_confirmation:
        errors.append('Password and confirmation must match')

    if errors:
        return jsonify({'errors': errors}), 422

    if User.query.filter_by(username=username).first():
        return jsonify({'errors': ['Username already exists']}), 422

    user = User(username=username)
    user.password_hash = password

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)

    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    errors = []

    if not username:
        errors.append('Username is required')
    if not password:
        errors.append('Password is required')

    if errors:
        return jsonify({'errors': errors}), 422

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        return jsonify({'errors': ['Invalid username or password']}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200


@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'errors': ['User not found']}), 404

    return jsonify(user.to_dict()), 200


# Notes CRUD endpoints

@app.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Query only the current user's notes with pagination
    pagination = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    notes = [note.to_dict() for note in pagination.items]

    return jsonify({
        'notes': notes,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }), 200


@app.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'errors': ['Note not found']}), 404

    return jsonify(note.to_dict()), 200


@app.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    errors = []

    if not title:
        errors.append('Title is required')
    if not content:
        errors.append('Content is required')

    if errors:
        return jsonify({'errors': errors}), 422

    note = Note(title=title, content=content, user_id=user_id)

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@app.route('/notes/<int:note_id>', methods=['PATCH'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'errors': ['Note not found']}), 404

    data = request.get_json()

    if 'title' in data:
        if not data['title']:
            return jsonify({'errors': ['Title cannot be empty']}), 422
        note.title = data['title']

    if 'content' in data:
        if not data['content']:
            return jsonify({'errors': ['Content cannot be empty']}), 422
        note.content = data['content']

    db.session.commit()

    return jsonify(note.to_dict()), 200


@app.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=note_id, user_id=user_id).first()

    if not note:
        return jsonify({'errors': ['Note not found']}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
