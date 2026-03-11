#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ResponseCode:
    SUCCESS = 200
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500


class CacheKey:
    PREFIX = "slack_translator"
    SET_MESSAGE_ID = "message_id"
    WORKER_PUSH = PREFIX + "_worker_push"
    CHANNEL_INFO = PREFIX + "_channel_info"
