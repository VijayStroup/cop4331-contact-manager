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

@router.get('/contact')
def get_all_contacts(id: str):
    contacts, error, message = db.get_contacts(id)

    if not error:
        return {'contacts': contacts, 'error': message}
    else:
        pass

@router.delete('/contact')
def delete_contact(id: str, name: str):
    error, message = db.del_contact(id, name)

    if not error:
        return {'error': message}
    else:
        pass