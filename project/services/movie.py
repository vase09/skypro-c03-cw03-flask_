from typing import List

from project.dao.models import Movie
from project.exceptions import ItemNotFound
from project.services.base import BaseService


class MovieService(BaseService):

    def get_all(self, page: str = None, status: str = None) -> List[Movie]:
        """
        Get all items from the db

        :param page: Page number (optional)
        :param status: 'New' if you want to sort movies by year
        """
        # Check parameter
        check_status = status == 'new'
        if not check_status:
            movies = self.dao.get_all(page, sort=False)

        # Get results
        movies = self.dao.get_all(page, sort=True)
        if not movies:
            raise ItemNotFound

        return movies
