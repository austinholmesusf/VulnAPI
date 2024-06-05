class AuthUser:

    def __init__(self, user_id: str, username: str, password_hash: str, permissions_group: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.permissions_group = permissions_group
