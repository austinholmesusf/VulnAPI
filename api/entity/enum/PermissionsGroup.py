def from_string(permissions_group_string):
    upper_group = permissions_group_string.upper()
    match upper_group:
        case 'USER':
            return PermissionsGroup.USER
        case 'ADMIN':
            return PermissionsGroup.ADMIN
        case _:
            raise ValueError('No such permissions group.')


class PermissionsGroup:
    USER = 0
    ADMIN = 1
