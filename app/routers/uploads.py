import asyncio
import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.schema.global_schema import ResponseSchema
from app.repository.auth_repo import JWTBearer

router = APIRouter(
    prefix="/api/v1/file-upload",
    tags=['upload-file'],
    dependencies=[Depends(JWTBearer())]
)

FILE_DESTINATION = "audio/eng/"


@router.post("/eng", response_model=ResponseSchema, response_model_exclude_none=True)
async def transcription_from_file(file: UploadFile):
    file_location = (
            FILE_DESTINATION
            + datetime.now().strftime("%Y_%m_%d_%H%M%S%f")
            + ".wav"
    )
    try:
        with open(file_location, 'wb+') as location:
            location.write(file.file.read())
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Uploading file failed or There is no audio/eng directory"
        )
    finally:
        file.file.close()
    return ResponseSchema(detail=f"Successfully uploaded {file.filename}", result="Hii")