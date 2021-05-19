from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix = '',
    tags = ['pages'],
    responses = {404: {'description': 'Not found'}},
)

templates = Jinja2Templates(directory="templates")


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
