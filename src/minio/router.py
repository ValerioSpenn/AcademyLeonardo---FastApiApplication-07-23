from fastapi import APIRouter
from fastapi import UploadFile, File


router = APIRouter()


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
        return {"Upload Image function"}


