from db import db
from fastapi import APIRouter, HTTPException

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
    error, message = db.new_user(name, password) 

    if not error:
        return {'user': user, 'error': message}
    else: 
        if error == 1:
            raise HTTPException(status_code=409, detail=message)
        else:
            raise HTTPException(status_code=500, detail=message)
