from pydantic import BaseModel


class ProductCreateDto(BaseModel):
    name: str
