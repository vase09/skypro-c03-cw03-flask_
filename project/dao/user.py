from typing import Union

from sqlalchemy.exc import NoResultFound

from .models import User
from .base import BaseDAO


class UserDAO(BaseDAO):

    def get_by_email(self, email: str) -> Union[User, None]:
        """
        Get user by the username

        :returns: User
        :returns: None, if no user found with the email passed
        """
        try:
            user = self.session.query(User).filter(User.email == email).one()
            return user
        except NoResultFound:
            return None

    def create(self, data: dict) -> User:
        """Add user to the database"""
        user = User(**data)
        self.session.add(user)
        self.session.commit()
        return user

    def update_by_email(self, data: dict, email: str) -> None:
        """Update user with data"""
        self.session.query(User).filter(User.email == email).update(data)
        self.session.commit()
