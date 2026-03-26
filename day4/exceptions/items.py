class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

class ItemAlreadyExistsException(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name