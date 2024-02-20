from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import JSONResponse
# from api.build_pinecone import init_pinecone
# from api.qa import retrieve, chat_complete
from hugging_api.build_pinecone import init_pinecone
from hugging_api.qa import retrieve, chat_complete
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define a message model to be used in the API
class Message(BaseModel):
    message: str


index = init_pinecone()
'''
flag:
1:simple prompt
2:cot
3:tot1
4:tot2
'''
flag = 1

@app.post("/api/message")
async def receive_message(message: Message):
    # 在这里处理接收到的消息
    print("Received message:", message.message)
    global flag
    flag = int(message.message)
    return {"status": "success"}

@app.post('/api/chat')
async def chat(request: Request, message: Message):
    print("submit message: ", message.message)
    # Get the user's message from the request
    query = message.message
    # get prompt from query and pinecone
    prompt = retrieve(query, index, flag)
    print('prompt:' + prompt)
    # get response
    response = chat_complete(prompt)['content']

    # convert unicode content to utf-8
    res_json = json.dumps(response, ensure_ascii=False)

    # 去掉res_json两侧的引号
    res_json = res_json[1:-1]
    print('response:' + res_json)
    return JSONResponse({'response': res_json})


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=9090)
