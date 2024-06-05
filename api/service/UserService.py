from api.exception.EndpointException import EndpointException
from api.repository import UserRepository


def get_user(user_id):
    result = UserRepository.get_user(user_id)
    if not result:
        raise EndpointException('No such user.', 404)
    return result
