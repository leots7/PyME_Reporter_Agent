class DatabaseError(Exception):
    def __init__(self, detail: str = "Database error occurred"):
        self.detail = detail
        super().__init__(self.detail)
