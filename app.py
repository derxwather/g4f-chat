import g4f
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import traceback
import uvicorn
import asyncio
import functools

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class msg(BaseModel):
    text: str

class img(BaseModel):
    text: str

def make_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return wrapper

@app.get("/")
async def home():
    return FileResponse("templates/index.html")

@app.post("/api/chat")
async def chat(msg: msg):
    try:
        @make_async
        def ask_gpt():
            return g4f.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": msg.text}],
                provider=g4f.Provider.ChatGptEs
            )
        
        answer = await ask_gpt()
        if not answer:
            print("Пустой ответ от GPT")
            raise Exception("нет ответа")
            
        return {"response": answer}
        
    except Exception as e:
        print(f"Что-то сломалось: {str(e)}")
        raise HTTPException(500, "все упало(")

@app.post("/api/generate-image") 
async def make_image(req: img):
    try:
        @make_async
        def get_image():
            return g4f.ChatCompletion.create(
                model="prodia",
                messages=[{"role": "user", "content": req.text}]
            )
        
        img_url = await get_image()
        if not img_url:
            print("Картинка не сгенерилась")
            raise Exception("картинка не получилась")
            
        return {"image_url": img_url}
        
    except Exception as e:
        print(f"Ошибка генерации: {str(e)}")
        raise HTTPException(500, "не смог сделать картинку(")

if __name__ == "__main__":
    print("Запускаю сервер...")
    uvicorn.run("app:app", host="localhost", port=8080, reload=True) 