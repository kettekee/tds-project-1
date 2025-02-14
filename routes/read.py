from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()


@router.get("")
async def read_file(path: str):
    # Allow only files under /data (or ./data in our project)
    if not path or not path.startswith("/data") and not path.startswith("./data"):
        raise HTTPException(
            status_code=404, detail="File path not allowed or missing")

    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(path, "r") as f:
            content = f.read()
        return PlainTextResponse(content, status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
