from sqlalchemy import create_engine

class DatabaseClient:
    def __init__(self) -> None:
        self.database = "postgresql://postgres:postgres@localhost:5433/fake_data"
        self.engine = create_engine(self.database)