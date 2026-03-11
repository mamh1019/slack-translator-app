#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class JSONResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # if type(response) is object:
        #     response = JSONResponse(status_code=200, content={"code": 200, "data": response})

        return response
