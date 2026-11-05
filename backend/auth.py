from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db, bcrypt
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"errors": ["Username and password are required"]}), 400

    username = username.strip()

    if not username or not password:
        return jsonify({"errors": ["Username and password are required"]}), 400

    if password != password_confirmation:
        return jsonify({"errors": ["Passwords do not match"]}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"errors": ["Username already exists"]}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(username=username, password_hash=hashed_password)

    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "token": token,
        "user": {"id": user.id, "username": user.username}
    }), 201
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"errors": ["Username and password are required"]}), 400

    user = User.query.filter_by(username=username.strip()).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"errors": ["Invalid username or password"]}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "token": token,
        "user": {"id": user.id, "username": user.username}
    }), 200
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"errors": ["User not found"]}), 404

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200