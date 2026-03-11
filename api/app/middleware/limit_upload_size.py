#!/usr/bin/env python
# -*- coding: utf-8 -*-

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import Response
from starlette import status


class LimitUploadSize:
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        self.app = app
        self.max_upload_size = max_upload_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            if scope["method"] == "POST":
                content_length = [data[1] for data in scope["headers"] if b"content-length" in data]

                if not content_length:
                    resp = Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
                    await resp(scope, receive, send)
                    return

                if int(content_length[0]) > self.max_upload_size:
                    resp = Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
                    await resp(scope, receive, send)
                    return

                await self.app(scope, receive, send)
                return

        await self.app(scope, receive, send)
