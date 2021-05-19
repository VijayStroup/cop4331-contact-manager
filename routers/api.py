from db import db
from fastapi import APIRouter

router = APIRouter(
    prefix = '/api',
    tags = ['api'],
    responses = {404: {'description': 'Not found'}},
)

@router.post('/user')
def new_user(name: str, password: str):
    user = {
        'name': name,
        'password': password
    }
    db.db.execute('insert into users values (?, ?)', (name, password,))

    return {'user': user}
