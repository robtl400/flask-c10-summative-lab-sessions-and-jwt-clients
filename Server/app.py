from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from models import db, bcrypt, User

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


if __name__ == '__main__':
    app.run(port=5555, debug=True)
