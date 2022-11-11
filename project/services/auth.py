import datetime
import calendar
from typing import Callable

import jwt
from flask import current_app, request
from flask_restx import abort

from .user import UserService
from ..exceptions import IncorrectPassword, InvalidToken


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def generate_tokens(self, credentials, is_refresh=False) -> dict:
        """
        Generate access and refresh JWT tokens

        :raises IncorrectPassword: If wrong password passed
        :raises ItemNotFound: If no user found with the email passed
        """

        # Unpack data and get user
        email_passed = credentials.get('email')
        password_passed = credentials.get('password')
        user = self.user_service.get_by_email(email_passed)

        # Check password
        if not is_refresh:
            password_is_correct = self.user_service.compare_passwords(user.password, password_passed)
            if not password_is_correct:
                raise IncorrectPassword

        # Prepare token data
        data = {
            'email': user.email
        }

        # Generate access token
        min_add = datetime.datetime.utcnow() \
                  + datetime.timedelta(minutes=current_app.config.get('TOKEN_EXPIRE_MINUTES'))
        data['exp']: int = calendar.timegm(min_add.timetuple())
        access_token = jwt.encode(data,
                                  current_app.config.get('JWT_SECRET'),
                                  algorithm=current_app.config.get('JWT_ALGORITHM'))

        # Generate refresh token
        days_add = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config.get('TOKEN_EXPIRE_DAYS'))
        data['exp']: int = calendar.timegm(days_add.timetuple())
        refresh_token = jwt.encode(data,
                                   current_app.config.get('JWT_SECRET'),
                                   algorithm=current_app.config.get('JWT_ALGORITHM'))

        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return tokens

    def get_email_from_token(self, token: str) -> str:
        """
        Get email from token

        :raise InvalidToken: if no valid token passed
        """
        try:
            data = jwt.decode(token,
                              current_app.config.get('JWT_SECRET'),
                              algorithms=[current_app.config.get('JWT_ALGORITHM')])
            email = data.get('email')
            return email
        except Exception:
            raise InvalidToken

    def approve_token(self, refresh_token: str) -> dict:
        """
        Approve refresh token and generate a new pair of tokens

        :raise InvalidToken: if no valid token passed
        """
        # Generate data for token and create new tokens
        credentials = {
            'email': self.get_email_from_token(refresh_token),
            'password': None
        }
        new_tokens = self.generate_tokens(credentials, is_refresh=True)
        return new_tokens

    @staticmethod
    def auth_required(func: Callable):
        """Check token passed is correct"""

        def wrapper(*args, **kwargs):
            # Check if authorization credentials were passed and get token
            if 'Authorization' not in request.headers:
                abort(401, 'No authorization data passed')

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]

            # Decode and check token
            try:
                jwt.decode(token, current_app.config.get('JWT_SECRET'),
                           algorithms=[current_app.config.get('JWT_ALGORITHM')])
            except Exception as e:
                abort(401, f'JWT decode error {e}')

            return func(*args, **kwargs)

        return wrapper
