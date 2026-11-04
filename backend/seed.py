from app import app
from extensions import db, bcrypt
from models import User, Asset


with app.app_context():
    # Create sample users if they do not already exist
    sample_users = [
        {
            "username": "demo_artist",
            "password": "Demo123!"
        },
        {
            "username": "studio_user",
            "password": "Studio123!"
        }
    ]

    users = {}

    for sample in sample_users:
        user = User.query.filter_by(
            username=sample["username"]
        ).first()

        if user is None:
            password_hash = bcrypt.generate_password_hash(
                sample["password"]
            ).decode("utf-8")

            user = User(
                username=sample["username"],
                password_hash=password_hash
            )

            db.session.add(user)

        users[sample["username"]] = user

    db.session.commit()

    # Sample 3D assets for each user
    sample_assets = {
        "demo_artist": [
            {
                "name": "Fantasy Warrior",
                "description": "A stylized 3D character model.",
                "category": "character",
                "format": "BLEND"
            },
            {
                "name": "Ancient Castle",
                "description": "A medieval environment asset.",
                "category": "environment",
                "format": "FBX"
            },
            {
                "name": "Metal Surface",
                "description": "A procedural metallic material.",
                "category": "material",
                "format": "OBJ"
            }
        ],
        "studio_user": [
            {
                "name": "Explosion Simulation",
                "description": "A rendered explosion simulation.",
                "category": "simulation",
                "format": "EXR"
            },
            {
                "name": "Sci-Fi Helmet",
                "description": "A futuristic hard-surface character asset.",
                "category": "character",
                "format": "BLEND"
            }
        ]
    }

    for username, assets in sample_assets.items():
        user = users[username]

        if not Asset.query.filter_by(user_id=user.id).first():
            for asset_data in assets:
                asset = Asset(
                    **asset_data,
                    user_id=user.id
                )
                db.session.add(asset)

    db.session.commit()

    print("Database seeded successfully!")