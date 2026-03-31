class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

class ItemAlreadyExistsException(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name

class UserAlreadyExistsException(Exception):
    def __init__(self, user_name: str):
        self.user_name = user_name

class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id

