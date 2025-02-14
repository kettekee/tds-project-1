from fastapi import APIRouter, HTTPException, Query
from services.task_parser import parse_and_execute_task

router = APIRouter()


@router.post("")
async def run_task(task: str = Query(..., description="Plain‑English task description")):
    if not task:
        raise HTTPException(
            status_code=400, detail="Task description is required")
    try:
        result = parse_and_execute_task(task)
        return {"result": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For production, consider logging the exception details
        raise HTTPException(status_code=500, detail="Internal server error")
