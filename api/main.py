#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv

load_dotenv(override=True, verbose=True)

import sys
import json
import traceback

sys.path.append("./app")

from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as api_router
from fastapi.responses import JSONResponse
from app.config.settings import Settings
from app.config.constants import ResponseCode


app = FastAPI(
    title="Slack Translator API",
    swagger_ui_parameters={"tryItOutEnabled": True},
    docs_url=None,
    redoc_url=None,
    # openapi_url="/openapi.json",
)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: Exception):
    response_message = {
        "code": exc.status_code,
        "message": exc.detail,
        "details": None,
    }
    response_json = json.dumps(response_message)

    return JSONResponse(
        status_code=exc.status_code,
        content=response_message,
    )


@app.exception_handler(Exception)
async def all_exception_handler(_: Request, exc: Exception):
    exc_type = type(exc).__name__
    exc_message = str(exc)
    full_message = f"{exc_type}: {exc_message}"
    response_message = {
        "code": ResponseCode.INTERNAL_SERVER_ERROR,
        "message": "An unexpected error occurred.",
        "details": full_message,
        "traceback": str(traceback.format_exc()),
    }

    return JSONResponse(
        status_code=ResponseCode.INTERNAL_SERVER_ERROR,
        content=response_message,
    )


@app.get("/uptime")
def uptime():
    import os

    sys_res = os.popen("uptime").read()[:-1]
    sys_res += "_N_"
    sys_res += os.popen("df -h").read()[:-1]
    return Response(content=sys_res, media_type="text/plain")


@app.get("/")
def root():
    return {"ENV": Settings.ENVIRONMENT, "v": "1.0.0"}
