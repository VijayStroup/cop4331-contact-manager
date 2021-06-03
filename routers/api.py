from clients import auth, db
from models.models import Contact, User
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(
    prefix = '/api',
    tags = ['api'],
    responses = {404: {'description': 'Not found'}}
)


@router.post('/user')
def new_user(user: User):
    user = {
        'username': user.username,
        'password': user.password
    }
    error, message = db.new_user(user) 

    if not error: return {'user': user, 'error': message}
    raise HTTPException(status_code=error, detail=message)


@router.get('/login')
def login(username: str, password: str):
    user, token, error, message = db.get_user(username, password)

    if not error: return {'user': user, 'token': token, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.post('/contact')
def new_contact(contact: Contact, user=Depends(auth.verify)):
    error, message = db.new_contact(user['id'], contact)

    if not error: return {'contact': contact, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.put('/contact')
def update_contact(contact_id: int, contact: Contact, user=Depends(auth.verify)):
    error, message = db.update_contact(user['id'], contact_id, contact)

    if not error: return {'contact': contact, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.delete('/contact')
def delete_contact(contact: Contact, user=Depends(auth.verify)):
    error, message = db.del_contact(user['id'], contact)

    if not error: return {'contact': contact, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.get('/contact')
def get_all_contacts(user=Depends(auth.verify)):
    contacts, error, message = db.get_contacts(user['id'])

    if not error: return {'contacts': contacts, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.get('/search')
def search_contacts(search: str, user=Depends(auth.verify)):
    contacts, error, message = db.search(user['id'], search)

    if not error: return {'contacts': contacts, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)
