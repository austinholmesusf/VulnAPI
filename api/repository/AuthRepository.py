from api.entity.AuthUser import AuthUser
from api.repository.UniversalRepository import UniversalRepository


UNIVERSAL = UniversalRepository(AuthUser, 'auth', ['user_id'])


def get_auth_user_count():
    return UNIVERSAL.get_record_count()


def get_user_id(username):
    result = UNIVERSAL.get_objects_intersection({'username': username})
    if result:
        return result[0].user_id


def get_password_hash(user_id):
    result = UNIVERSAL.get_objects_intersection({'user_id': user_id})
    if result:
        return result[0].password_hash


def get_permissions_group(user_id):
    result = UNIVERSAL.get_objects_intersection({'user_id': user_id})
    if result:
        return result[0].permissions_group


def create_auth_user(auth_user):
    UNIVERSAL.create_object(auth_user)
