import base64
import hashlib
import hmac

from flask import current_app
from werkzeug.exceptions import MethodNotAllowed

from project.dao.models import User
from project.exceptions import UserAlreadyExists, IncorrectPassword, ItemNotFound
from project.services.base import BaseService


class UserService(BaseService):

    def get_by_email(self, email: str) -> User:
        """
        Get user data by username

        :raises ItemNotFound: If no user found with the email passed
        """
        user = self.dao.get_by_email(email)
        if not user:
            raise ItemNotFound
        return user

    def create(self, data: dict) -> User:
        """Add user to the database"""
        # Check if user already exists
        user = self.dao.get_by_email(data.get('email'))
        if user:
            raise UserAlreadyExists

        # Hash password and add user to the database
        data['password'] = self.create_hash(data.get('password'))
        user = self.dao.create(data)
        return user

    def update_info(self, data: dict, email: str) -> None:
        """
        Partially update user information

        :raises MethodNotAllowed: If changing email or password
        """
        # Check user exists
        self.get_by_email(email)
        # Check data is okay
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update_by_email(data, email)
        else:
            raise MethodNotAllowed

    def update_password(self, data: dict, email: str) -> None:
        """
        Partially update user information

        :raises MethodNotAllowed: If wrong fields passed
        "raises IncorrectPassword: If password isn't correct
        """

        # Check data is okay
        user = self.get_by_email(email)
        current_password = data.get('old_password')
        new_password = data.get('new_password')

        if None in [current_password, new_password]:
            raise MethodNotAllowed

        if not self.compare_passwords(user.password, current_password):
            raise IncorrectPassword

        # Hash password and update
        data = {
            'password': self.create_hash(new_password)
        }
        self.dao.update_by_email(data, email)

    def create_hash(self, password: str) -> bytes:
        """Create sha256 password hash"""
        hash_digest: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            current_app.config.get('PWD_HASH_SALT'),
            current_app.config.get('PWD_HASH_ITERATIONS')
        )
        return hash_digest

    def compare_passwords(self, password_hash: str, password_passed: str) -> bool:
        """Compare password passed with the user password in db"""
        passed_hash: bytes = self.create_hash(password_passed)
        is_equal: bool = hmac.compare_digest(password_hash, passed_hash)
        return is_equal
