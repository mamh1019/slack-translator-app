#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from config.settings import Settings


class RedisClient:
    _client = None  # Redis 연결 객체 저장 (클래스 변수)

    def __init__(self):
        if not RedisClient._client:
            RedisClient._client = redis.Redis(
                host=Settings.Redis.host, port=Settings.Redis.port, db=0, decode_responses=True
            )

    @classmethod
    def set(cls, key: str, value: str, ex: int = None):
        return cls._client.set(key, value, ex=ex)

    @classmethod
    def get(cls, key: str):
        return cls._client.get(key)

    @classmethod
    def delete(cls, key: str):
        return cls._client.delete(key)

    @classmethod
    def exists(cls, key: str):
        return cls._client.exists(key)

    @classmethod
    def flush_all(cls):
        return cls._client.flushall()

    @classmethod
    def lpush(cls, key: str, value: str):
        return cls._client.lpush(key, value)
