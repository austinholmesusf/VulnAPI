import uuid

import api.config.Config as Config
import hashlib
import re
import api.repository.AuthRepository as AuthRepository
from api.entity.AuthJWT import AuthJWT
from api.entity.AuthUser import AuthUser
from api.entity.User import User
from api.entity.enum.PermissionsGroup import PermissionsGroup
from api.exception.AuthException import AuthException
from api.repository import UserRepository


def validate_password(password: str) -> bool:
    """
    The following criteria will be evaluated:
    - Must be between 8-12 characters (inclusive)
    - Must contain at least one capital letter.
    - Must contain at least one special (non-alphanumeric) character.
    """
    return bool(re.search(r'(?=.*\d)(?=.*[^A-Za-z0-9])(?=.*[A-Z])(^.{8,12}$)', password))


def hash_password(password: str) -> str:
    return hashlib.sha512(str.encode(password + Config.SALT), usedforsecurity=True).hexdigest()


def create_user_id() -> str:
    return str(uuid.uuid4())


def login(username: str, password: str) -> str:
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)

    user_id = AuthRepository.get_user_id(username)
    if not user_id:
        raise AuthException("Invalid username or password.")
    stored_hash = AuthRepository.get_password_hash(user_id)
    if stored_hash != hash_password(password):
        raise AuthException("Invalid username or password.")

    permissions_group = AuthRepository.get_permissions_group(user_id)
    return AuthJWT(user_id, permissions_group).encode()


def signup(username: str, password: str, first_name: str, last_name: str) -> str:
    if not username or not password:
        raise AuthException("Username or password are not provided.", 400)
    if not first_name or not last_name:
        raise AuthException("First or last name are not provided.", 400)
    if not validate_password(password):
        raise AuthException("Password does not meet requirements.", 400)
    if AuthRepository.get_user_id(username):
        raise AuthException("Username already exists.", 409)

    user_id = create_user_id()

    auth_user = AuthUser(user_id, username, hash_password(password), 'users')
    AuthRepository.create_auth_user(auth_user)

    user = User(user_id, username, first_name, last_name)
    UserRepository.create_user(user)

    return AuthJWT(user_id, PermissionsGroup.USER).encode()
