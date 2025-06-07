from typing import Union

from fastapi import FastAPI # type: ignore
from app.middlewares.cors_middleware import add_cors_middleware
from s3_presigned import router as s3_router
from compress_files_from_s3 import compress_files


app = FastAPI()

add_cors_middleware(app)
app.include_router(s3_router)
app.add_api_route("/compress", compress_files, methods=["GET"]) 


@app.get("/")
def read_root():
    return {"Hello": "World"}

