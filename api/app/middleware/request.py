#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import time
from starlette.middleware.base import BaseHTTPMiddleware


class RequestMiddleware(BaseHTTPMiddleware):
    async def before_request(self, request):
        # request.state.start_time = time.time()
        pass

    async def after_request(self, _, response):
        # elapsed_time = time.time() - request.state.start_time

        return response

    async def dispatch(self, request, call_next):
        await self.before_request(request)

        try:
            response = await call_next(request)
        except Exception as exc:
            # send error log (webhook)
            # ....
            # throw exception to higher level
            raise exc from None

        return await self.after_request(request, response)
