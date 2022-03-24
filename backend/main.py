import time

from fastapi import FastAPI

from .routers import projects, videos

app = FastAPI()
app.include_router(projects.router, prefix="/projects")
app.include_router(videos.router, prefix="/videos")


@app.middleware("http")
async def print_process_time(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(f"took: {time.time() - start_time:.2f}s")
    return response


@app.get("/")
def status():
    return {"status": "running"}
