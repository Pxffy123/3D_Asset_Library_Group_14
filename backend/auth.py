from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from extensions import db, bcrypt
from models import User

auth_bp = Blueprint("auth", _name_)

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