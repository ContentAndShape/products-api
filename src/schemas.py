from typing import List

from pydantic import BaseModel


class Brand(BaseModel):
    name: str
    slug: str


class Category(BaseModel):
    name: str
    slug: str


class Leftover(BaseModel):
    size: str
    count: int
    price: int


class Product(BaseModel):
    title: str
    sku: str
    color: str | None
    color_code: str | None
    brand: Brand
    sex: str
    root_category: Category
    price: int
    discount_price: int
    in_the_sale: bool
    size_table_type: str
    leftovers: List[Leftover]


class ProductsResponse(BaseModel):
    products: List[Product]
