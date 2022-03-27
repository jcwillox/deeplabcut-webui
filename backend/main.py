import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import projects, videos

app = FastAPI()
app.include_router(projects.router, prefix="/projects")
app.include_router(videos.router, prefix="/videos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def print_process_time(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(f"took: {time.time() - start_time:.2f}s")
    return response


@app.get("/")
def status():
    return {"status": "running"}
