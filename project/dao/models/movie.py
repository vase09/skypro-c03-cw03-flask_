from marshmallow import Schema, fields

from project.dao.models import GenreSchema, DirectorSchema
from project.dao.models.base import BaseMixin
from project.setup_db import db


class Movie(BaseMixin, db.Model):
    __tablename__ = 'movie'

    title = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    trailer = db.Column(db.Text(), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"), nullable=False)

    genre = db.relationship("Genre")
    director = db.relationship("Director")

    def __repr__(self):
        return f"<Movie '{self.title.title()}'>"


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)
