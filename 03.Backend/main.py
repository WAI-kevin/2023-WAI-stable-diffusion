from fastapi import FastAPI, APIRouter, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src import model
from typing import List
import os
# from src import router

server = FastAPI()

@server.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello World"
    }

origins = ["*"]
# [
#     "http://172.30.112.1:3000",
#     "http://10.177.197.177:3000",
# ]

# api 권한 등의 설정
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

com_router = APIRouter()

# 입력 받을 데이터 사전 정의
class Book(BaseModel):
    text: str
    price: int

    

@com_router.post("/book")
async def GENERATE_TAB(book: Book):
    convert = model.ClsProcess()
    prompt_text = convert.preprocess(book.text)
    print(prompt_text)
    return convert.text_to_image(prompt_text, '111')


# 프론트 테스트 용
@server.post("/ImgTest")
async def fileUpload(in_files: List[UploadFile] = File()):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(BASE_DIR,'static/')
    IMG_DIR = os.path.join(STATIC_DIR,'images/')
    
    print(IMG_DIR)
    for file in in_files:
        # contents = await item_file.read()
        file_location = os.path.join(IMG_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    return {"filename" : [item_file.filename for item_file in in_files]}

server.include_router(com_router)
