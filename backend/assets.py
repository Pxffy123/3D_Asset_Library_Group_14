from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Asset

assets_bp = Blueprint("assets", __name__)


def asset_to_dict(asset):
    return {
        "id": asset.id,
        "name": asset.name,
        "description": asset.description,
        "category": asset.category,
        "format": asset.format,
        "user_id": asset.user_id
    }
@assets_bp.route("/assets", methods=["GET"])
@jwt_required()
def get_assets():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1 or per_page > 100:
        return jsonify({"error": "Invalid pagination values"}), 400

    pagination = Asset.query.filter_by(
        user_id=user_id
    ).order_by(Asset.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "items": [asset_to_dict(asset) for asset in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": pagination.page,
        "per_page": pagination.per_page
    }), 200
@assets_bp.route("/assets", methods=["POST"])
@jwt_required()
def create_asset():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "description", "category", "format"]

    for field in required_fields:
        if not isinstance(data.get(field), str) or not data[field].strip():
            return jsonify({
                "error": f"{field} is required and must be text"
            }), 400

    asset = Asset(
        name=data["name"].strip(),
        description=data["description"].strip(),
        category=data["category"].strip(),
        format=data["format"].strip(),
        user_id=user_id
    )

    db.session.add(asset)
    db.session.commit()

    return jsonify(asset_to_dict(asset)), 201