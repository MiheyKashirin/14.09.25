import secrets
import string
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import json
import aiofiles
import os
import uvicorn
import motor.motor_asyncio


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

mongo_host = os.environ.get('MONGO_HOST', 'localhost')
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://admin:password@{mongo_host}:27017')
db = mongo_client.shortener
urls_collection = db.urls





@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})


from fastapi.responses import RedirectResponse


@app.get('/{short_url}')
async def short_url_handler(short_url: str):
    urls_data = await urls_collection.find_one({'short_url': short_url})
    if urls_data:
        await urls_collection.update_one(
            {'short_url': short_url},
            {'$inc': {'clicks': 1}}
        )
        return RedirectResponse(urls_data['long_url'])
    return {"error": "Ссылка не найдена"}


@app.post('/')
async def create_url(longurl: Annotated[str, Form()]):
    alphabet = string.ascii_letters + string.digits
    short_url = ''.join(secrets.choice(alphabet) for _ in range(6))
    await urls_collection.insert_one({'short_url': short_url, 'long_url': longurl, 'clicks': 0})
    return {"short_url": short_url, "long_url": longurl}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
