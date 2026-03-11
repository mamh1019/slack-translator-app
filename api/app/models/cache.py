#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from libs.redis_client import RedisClient
from config.constants import CacheKey


class Cache:
    def __init__(self):
        self.redis_client = RedisClient()

    def set(self, key, value, expired=3600 * 24 * 7):
        self.redis_client.set(key, value, expired)

    def get(self, key):
        return self.redis_client.get(key)

    def lpush(self, key, value: dict):
        self.redis_client.lpush(key, json.dumps(value))

    def get_message_id_key(self, channel_id):
        return f"{CacheKey.PREFIX}_{CacheKey.SET_MESSAGE_ID}_{channel_id}"

    def get_channel_info_key(self, channel_id):
        return f"{CacheKey.CHANNEL_INFO}_{channel_id}"

    def get_channel_info(self, channel_id: str):
        key = self.get_channel_info_key(channel_id)
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set_channel_info(self, channel_id: str, target_lang: str = "EN"):
        key = self.get_channel_info_key(channel_id)
        value = json.dumps({"target_lang": target_lang.upper()})
        self.redis_client.set(key, value)

    def update_channel_info(self, channel_id: str, channel_name: str, target_lang: str):
        key = self.get_channel_info_key(channel_id)
        value = json.dumps({"target_lang": target_lang.upper(), "channel_name": channel_name})
        self.redis_client.set(key, value)
