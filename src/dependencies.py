from typing import Dict, List

from pydantic import BaseModel


class FilterParams(BaseModel):
    title: str | None
    category: str | None
    brand: str | None
    price_from: int | None
    price_to: int | None
    size: str | None

    def get_query(self) -> Dict:
        """Адаптирует параметры запроса в объект-запрос, распознаваемый драйвером Mongo."""
        adapted_query_object = {}

        if self.title is not None:
            adapted_query_object["title"] = self.title

        if self.size is not None:
            adapted_query_object["leftovers"] = {"$elemMatch": {
                "size": {"$eq": self.size}, 
                "count": {"$gt": 0}
                }
            }
        else:
            adapted_query_object["leftovers.count"] = {"$gt": 0}


        if self.category is not None:
            adapted_query_object["root_category.name"] = self.category

        if self.brand is not None:
            adapted_query_object["brand.name"] = self.brand

        if self.price_from is not None or self.price_to is not None:
            if self.price_from is not None and self.price_to is None:
                adapted_query_object["price"] = {"$gte": self.price_from}
            elif self.price_to is not None and self.price_from is None:
                adapted_query_object["price"] = {"$lte": self.price_to}
            else:
                adapted_query_object["price"] = {"$gte": self.price_from, "$lte": self.price_to}
        
        return adapted_query_object
    
    def get_pipeline(self) -> List:
        raise NotImplementedError()
        conditions_list = []

        if self.brand is not None:
            conditions_list.append({"brand.name": {"$eq": self.brand}})
        
        if self.category is not None:
            conditions_list.append({"root_category.name": {"$eq": self.category}})

        if self.price_from is not None or self.price_to is not None:
            if self.price_from is not None and self.price_to is None:
                conditions_list.append({"price": {"$gte": self.price_from}})
            elif self.price_to is not None and self.price_from is None:
                conditions_list.append({"price": {"$lte": self.price_to}})
            else:
                conditions_list.append({"price": {"$gte": self.price_from, "$lte": self.price_to}})

        leftovers_conditions_list = []
        
        leftovers_conditions_list.append({"$gt": ["$$leftover.count", 0]})

        if self.size is not None:
            leftovers_conditions_list.append({"$eq": ["$$leftover.size", self.size]})
            leftovers_conditions_list.append({"$gt": ["$$leftover.count", 0]})

        return [
            {"$match": {"$and": conditions_list}},
            {"$project": {
                "leftovers": {"$filter": {
                    "input": "$leftovers",
                    "as": "leftover",
                    "cond": {"$and": leftovers_conditions_list}
                }}
            }}
        ]


def get_filter_params(
    price_from: int | None = None,
    price_to: int | None = None,
    category: str | None = None,
    brand: str | None = None,
    size: str | None = None,
    title: str | None = None, 
) -> FilterParams:
    return FilterParams(
        price_from=price_from,
        price_to=price_to,
        category=category,
        brand=brand,
        size=size,
        title=title,
    )