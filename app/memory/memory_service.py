class MemoryService:
    """
    Simple in-memory storage (upgrade to PostgreSQL later)
    """

    def __init__(self):
        self.storage = []

    def save(self, data: dict):
        self.storage.append(data)

    def get_all(self):
        return self.storage

    def get_last(self):
        if self.storage:
            return self.storage[-1]
        return None