from typing import Optional
from fastapi import Request, APIRouter, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from clients import auth, db

router = APIRouter(
    prefix = '',
    tags = ['pages'],
    responses = {404: {'description': 'Not found'}},
)

templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
def home(request: Request, token: Optional[str] = Cookie(None)):
    try: user = auth.decode_token(token)
    except HTTPException:
        return RedirectResponse('/login')
    return templates.TemplateResponse(
        'home.html',
        {'request': request, 'username': user['username']}
    )


@router.get('/login', response_class=HTMLResponse)
def login(request: Request, token: Optional[str] = Cookie(None)):
    try: auth.decode_token(token)
    except HTTPException:
        return templates.TemplateResponse('login.html', {'request': request})
    return RedirectResponse('/')


@router.get('/register', response_class=HTMLResponse)
def register(request: Request, token: Optional[str] = Cookie(None)):
    try: auth.decode_token(token)
    except HTTPException:
        return templates.TemplateResponse('register.html', {'request': request})
    return RedirectResponse('/')


@router.get('/contacts', response_class=HTMLResponse)
def contacts(request: Request, token: Optional[str] = Cookie(None)):
    try: user = auth.decode_token(token)
    except HTTPException: return RedirectResponse('/login')

    contacts, error, _ = db.get_contacts(user['id'])
    if not error:
        return templates.TemplateResponse(
            'contacts.html',
            {'request': request, 'contacts': contacts, 'username': True}
        )
    else: RedirectResponse('/')
