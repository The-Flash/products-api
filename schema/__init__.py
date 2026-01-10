from sqlmodel import create_engine, SQLModel, Field


class Model:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(
            self.db_url, max_overflow=0, pool_size=1, pool_pre_ping=True
        )


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class ProductCreate(SQLModel):
    name: str
