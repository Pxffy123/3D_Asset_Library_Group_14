
from flask import Flask

from extensions import db, migrate, bcrypt, jwt


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.update({
    "SQLALCHEMY_DATABASE_URI": "sqlite:///asset_library.db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "JWT_SECRET_KEY": "temporary-development-secret"
    })

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import models so Flask-Migrate can discover them.
    import models

    # Register authentication routes.
    from auth import auth_bp
    app.register_blueprint(auth_bp)
    from assets import assets_bp
    app.register_blueprint(assets_bp)

    @app.route("/")
    def home():
        return {"message": "3D Asset Library API is running!"}

    return app


app = create_app()



if __name__ == "__main__":
    app.run(port=5555, debug=True)

