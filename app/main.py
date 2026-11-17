from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .image_utils import load_image_from_url, load_image_from_file
from .inference import predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或填写你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    url: str

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        image = load_image_from_file(await file.read())
        result = predict(image)
        return JSONResponse(content={
            "code": 200,
            "message": "检测成功",
            "payload": result
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"上传图片处理失败: {str(e)}")

@app.post("/check-url")
async def check_url(input: UrlInput):
    try:
        image = load_image_from_url(input.url)
        result = predict(image)
        return JSONResponse(content={
            "code": 200,
            "message": "检测成功",
            "payload": result
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"URL图片处理失败: {str(e)}")
