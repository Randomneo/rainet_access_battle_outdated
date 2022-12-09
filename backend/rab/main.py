import asyncio
from typing import AsyncIterator

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from .config import configer
from .database import async_session
from .models import User
from .security import check_password

app = FastAPI()
lock = asyncio.Lock()


class Redirect(Exception):
    def __init__(self, url):
        self.url = url


async def get_session() -> AsyncIterator[AsyncSession]:    # pragma: no cover
    async with async_session() as session:
        yield session


async def get_user_by_id(session, user_id):
    return (await session.execute(select(User).filter(User.id == user_id))).scalar()


async def get_user(request: Request = None, websocket: WebSocket = None, session=Depends(get_session)) -> User | None:
    method = request or websocket
    if not method or 'user_id' not in method.session:
        return None
    return await get_user_by_id(session, method.session['user_id'])


app.add_middleware(SessionMiddleware, secret_key=configer.get('SECRET_KEY'))


@app.exception_handler(Redirect)
async def redirect(request, exc):
    return RedirectResponse(exc.url, status_code=302)


@app.get('/')
async def root(session=Depends(get_session)):
    raise Redirect(app.url_path_for('home'))


@app.get('/home', response_class=HTMLResponse)
async def home(request: Request, user: User = Depends(get_user)):
    return {
        'user': user,
    }


@app.get('/login', response_class=HTMLResponse, name='get_login')
async def get_login(request: Request):
    return {}


@app.get('/status')
async def status(request: Request, session=Depends(get_session)):
    if 'user_id' not in request.session:
        return None
    user = (await session.execute(select(User).filter(User.id == request.session['user_id']))).scalar()
    return user.username


@app.post('/login', response_class=HTMLResponse, name='post_login')
async def post_login(
        request: Request,
        username: str = Form(),
        password: str = Form(),
        redirect_to: str = Form(default=None),
        session=Depends(get_session),
):
    redirect_to = redirect_to or app.url_path_for('home')
    user = (await session.execute(select(User).filter(User.username == username))).scalar()
    if user and check_password(password, user.password):
        request.session['user_id'] = user.id
        raise Redirect(redirect_to)

    return {
        'error': True,
        'username': username,
        'redirect_to': redirect_to,
    }


@app.get('/logout')
async def logout(request: Request):
    del request.session['user_id']
    raise Redirect(app.url_path_for('home'))
