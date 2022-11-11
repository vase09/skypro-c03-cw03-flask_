from typing import List

from project.dao.models import Favourite
from project.exceptions import ItemAlreadyExists, ItemNotFound
from project.services.base import BaseService


class FavouriteService(BaseService):

    def add_favourite(self, user_id, movie_id) -> None:
        """
        Add movie to user favourites

        :raises ItemAlreadyExists: If movie already in favouries
        """

        data = {
            'user_id': user_id,
            'movie_id': movie_id
        }
        if self.dao.get_favourite(user_id, movie_id):
            raise ItemAlreadyExists

        self.dao.create(data)

    def delete_favourite(self, user_id, movie_id) -> None:
        """
        Delete movie from user favouries

        :raises ItemNotFound: If movie not in favourites
        """

        favourite = self.dao.get_favourite(user_id, movie_id)
        if not favourite:
            raise ItemNotFound

        uid = favourite[0].id
        self.dao.delete(uid)

    def get_user_favourites(self, user_id) -> List[Favourite]:
        """
        Get all user's favourites

        :raises ItemNotFound: If no items found
        :returns: List of user favourites
        """

        favourites = self.dao.get_user_favourites(user_id)

        # if not favourites:
        #     raise ItemNotFound

        return favourites
