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

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('mainpage.html', {"request": request})


@app.get('/{short_url}')
async def short_url_handler(short_url: str):
    async with aiofiles.open('urls.json', mode='r') as f:
        content = await f.read()
        urls_data = json.loads(content) if content else {}
    longurl = urls_data.get(short_url)
    if longurl:
        return RedirectResponse(longurl)
    return {"error": "Not found"}


@app.post('/')
async def create_url(longurl: Annotated[str, Form()]):
    alphabet = string.ascii_letters + string.digits
    short_url = ''.join(secrets.choice(alphabet) for _ in range(6))
    if not os.path.exists('urls.json'):
        urls_data = {}
    else:
        async with aiofiles.open('urls.json', mode='r') as f:
            content = await f.read()
            urls_data = json.loads(content) if content else {}
    urls_data[short_url] = longurl
    async with aiofiles.open('urls.json', mode='w') as f:
        await f.write(json.dumps(urls_data, indent=4))
    return {"short_url": short_url, "longurl": longurl}



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
