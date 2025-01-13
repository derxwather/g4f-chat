import g4f
from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import traceback
import uvicorn
import asyncio
import functools

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static"), name="static")

class msg(BaseModel):
    text: str

class img(BaseModel):
    text: str

def run_async(f):
    @functools.wraps(f)
    async def wrap(*args, **kwargs):
        return await asyncio.get_running_loop().run_in_executor(None, functools.partial(f, *args, **kwargs))
    return wrap

@app.get("/")
async def main():
    return FileResponse("templates/index.html")

@app.post("/api/chat")
async def chat(m: msg):
    try:
        @run_async
        def get_answer():
            return g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": m.text}],
                provider=g4f.Provider.ChatGptEs,
            )
        
        res = await get_answer()
        if not res:
            raise Exception("пусто")
        return {"response": res}
    except:
        err = traceback.format_exc()
        print(f"ошибка: {err}")
        raise HTTPException(500, "ошибка")

@app.post("/api/generate-image")
async def img_gen(m: img):
    try:
        @run_async
        def get_img():
            return g4f.ChatCompletion.create(
                model="prodia",
                messages=[{"role": "user", "content": m.text}],
            )
        
        url = await get_img()
        if not url:
            raise Exception("пусто")
        return {"image_url": url}
    except:
        err = traceback.format_exc()
        print(f"ошибка: {err}")
        raise HTTPException(500, "ошибка")

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True) 