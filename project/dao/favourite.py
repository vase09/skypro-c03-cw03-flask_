from typing import List

from .base import BaseDAO
from .models import Favourite, Movie


class FavouriteDAO(BaseDAO):

    def get_favourite(self, user_id, movie_id) -> List[Favourite]:
        """Get specific favourite"""
        data = self.session.query(Favourite)\
            .filter(Favourite.user_id == user_id, Favourite.movie_id == movie_id)\
            .all()
        return data

    def get_user_favourites(self, user_id) -> List[Favourite]:
        """Get all favourites of the user"""
        data = self.session.query(Movie).join(Favourite)\
            .filter(Favourite.user_id == user_id, Movie.id == Favourite.movie_id)\
            .all()
        return data
