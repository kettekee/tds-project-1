from fastapi import FastAPI
from routes.run import router as run_router
from routes.read import router as read_router

app = FastAPI(title="LLM-based Automation Agent")

app.include_router(run_router, prefix="/run")
app.include_router(read_router, prefix="/read")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
