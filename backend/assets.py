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