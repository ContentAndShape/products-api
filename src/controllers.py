from fastapi import APIRouter, Depends, Request

from schemas import ProductsResponse
from dependencies import FilterParams, get_filter_params
from db import get_documents
from db_collections import Collections


router = APIRouter()


@router.get(
    "/products",
    response_model=ProductsResponse,
    status_code=200,
)
async def get_products(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    filter_params: FilterParams = Depends(get_filter_params),
) -> ProductsResponse:
    products = await get_documents(
        db=request.app.state.db,
        collection=Collections.products.value,
        filter_params=filter_params,
        skip=skip,
        limit=limit,
    )
    return ProductsResponse(
        products=products,
    )
