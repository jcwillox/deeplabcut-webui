import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import managers
from .config import get_settings
from .routers import projects, videos

app = FastAPI()
app.include_router(projects.router, prefix="/projects")
app.include_router(videos.router, prefix="/videos")

managers.register_events(app)


@app.middleware("http")
async def print_process_time(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(f"took: {time.time() - start_time:.2f}s")
    return response


@app.middleware("http")
async def token_auth(request: Request, call_next):
    token = get_settings().token
    if token:
        request_token = request.query_params.get("token")
        if request_token != token:
            return JSONResponse({"error": "not authorised"}, status_code=401)
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_status():
    return {"status": "running"}


def main(**kwargs):
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        ssl_certfile=settings.ssl_certfile,
        ssl_keyfile=settings.ssl_keyfile,
        **kwargs,
    )


if __name__ == "__main__":
    main()
