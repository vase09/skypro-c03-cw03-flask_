from .dao import MovieDAO, DirectorDAO, GenreDAO, UserDAO, FavouriteDAO
from .dao.models import Movie, Genre, Director, User, Favourite
from .services import MovieService
from .services import DirectorService
from .services import GenreService
from .services import UserService
from .services import AuthService
from .services import FavouriteService
from .setup_db import db

# Create DAO
movie_dao = MovieDAO(session=db.session, model=Movie)
director_dao = DirectorDAO(session=db.session, model=Director)
genre_dao = GenreDAO(session=db.session, model=Genre)

user_dao = UserDAO(session=db.session, model=User)
favourite_dao = FavouriteDAO(session=db.session, model=Favourite)

# Create services
movie_service = MovieService(dao=movie_dao)
director_service = DirectorService(dao=director_dao)
genre_service = GenreService(dao=genre_dao)

user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service=user_service)
favourite_service = FavouriteService(dao=favourite_dao)
