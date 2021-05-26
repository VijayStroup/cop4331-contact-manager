from db import db
from middleware.auth import auth
from models.models import Contact
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(
    prefix = '/api',
    tags = ['api'],
    responses = {404: {'description': 'Not found'}}
)


@router.post('/user')
def new_user(username: str, password: str):
    user = {
        'username': username,
        'password': password
    }
    error, message = db.new_user(user) 

    if not error: return {'user': user, 'error': message}
    else: raise HTTPException(status_code=error, detail=message)


@router.post('/login')
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
def update_contact(contact: Contact, user=Depends(auth.verify)):
    error, message = db.update_contact(user['id'], contact['id'], contact)

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
