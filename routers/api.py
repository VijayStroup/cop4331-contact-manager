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


@router.post('/contact')
def new_contact(id: str, name: str):
    contact = {
        'id': 1, #per request in github
        'name': name
    }

    error, message = db.new_contact(id, name)

    if not error:
        return {'id': 1, 'error': message}
    else:
        #status_code=500 because I'm not sure what specific issue would be raised
        raise HTTPException(status_code=500, detail=message)

    return {'user': user}


@router.get('/contact')
def get_all_contacts(id: str):
    contacts, error, message = db.get_contacts(id)

    if not error:
        return {'contacts': contacts, 'error': message}
    else:
        pass


@router.delete('/contact')
def delete_contact(id: str, name: str):
    contact, error, message = db.del_contact(id, name)

    if not error:
        return {'contact': contact, 'error': message}
    else:
        pass
