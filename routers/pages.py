from fastapi import APIRouter

router = APIRouter(
    prefix = '',
    tags = ['pages'],
    responses = {404: {'description': 'Not found'}},
)
