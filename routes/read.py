from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()


@router.get("")
async def read_file(path: str):
    # Map '/data' to './data'
    if path.startswith("/data"):
        path = "." + path

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(path, "r") as f:
            content = f.read()
        return PlainTextResponse(content, status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
