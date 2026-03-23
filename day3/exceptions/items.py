class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id