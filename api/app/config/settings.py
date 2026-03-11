#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class DB_Config:
    def __init__(self, db_host, db_user, db_pass, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name


class Settings:
    ENVIRONMENT = os.getenv("PRODUCTION")

    class Redis:
        host: str = os.getenv("REDIS_HOST")
        port: int = os.getenv("REDIS_PORT")
