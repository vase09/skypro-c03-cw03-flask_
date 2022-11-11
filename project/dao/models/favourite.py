from marshmallow import Schema, fields

from project.dao.models import MovieSchema
from project.dao.models.base import BaseMixin
from project.setup_db import db


class Favourite(BaseMixin, db.Model):
    __tablename__ = 'favourite'

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"),  nullable=False)

    user = db.relationship("User")
    movie = db.relationship("Movie")


class FavouriteSchema(Schema):
    user_id = fields.Int()
    movie = fields.Nested(MovieSchema)
