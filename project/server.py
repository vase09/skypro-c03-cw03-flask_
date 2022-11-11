from flask import Flask
from flask_cors import CORS
from flask_restx import Api


from project.setup_db import db, migrate
from project.views import (movie_ns, director_ns, genre_ns,
                           auth_ns, user_ns, favourite_ns)

api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 4",
    doc="/docs",
)

cors = CORS()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Register extensions
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Register end-points
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(favourite_ns)

    return app
