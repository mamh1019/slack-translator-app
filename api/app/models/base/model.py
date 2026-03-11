#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from app.config import DB_Config

## Type Def
from pymysql.cursors import DictCursor
from pymysql.connections import Connection
from pandas import DataFrame

""" pymysql 은 동기식이라 await 필요 없음
"""


class Model:
    _conn_db: Connection = None
    _curs_db: DictCursor = None

    def __init__(self, db_setting: DB_Config):
        """Create RDBMS Connection

        :param env_mysql_section: env.ini database section key
        """
        self._conn_db = pymysql.connect(
            host=db_setting.db_host,
            user=db_setting.db_user,
            password=db_setting.db_pass,
            db=db_setting.db_name,
            charset="utf8",
        )
        self._curs_db = self._conn_db.cursor(pymysql.cursors.DictCursor)
        self._insert_db = create_engine(
            f"mysql+pymysql://{db_setting.db_user}:{db_setting.db_pass}@{db_setting.db_host}/{db_setting.db_name}"
        )

    def __del__(self):
        if self._conn_db:
            self._curs_db.close()
            self._conn_db.close()

    @property
    def conn_db(self) -> Connection:
        return self._conn_db

    @property
    def curs_db(self) -> DictCursor:
        return self._curs_db

    def insert_all(self, sql: str, params: list) -> bool:
        """Base Query"""
        if len(params) <= 0:
            return
        self._curs_db.executemany(sql, params)
        return self._conn_db.commit()

    def commit(self, sql):
        self._curs_db.execute(sql)
        return self._conn_db.commit()

    def fetchall(self, sql) -> list:
        self._curs_db.execute(sql)
        return self._curs_db.fetchall()

    def fetchone(self, sql) -> dict:
        self._curs_db.execute(sql)
        return self._curs_db.fetchone()

    def dataframe(self, sql) -> DataFrame:
        return pd.read_sql(sql, self._conn_db).replace([np.nan], [None])

    def pd_insert(self, df, name, mode="append"):
        return df.to_sql(con=self._insert_db, name=name, if_exists=mode, index=False)

    def batch_insert(self, sql, batch_insert_vars: list[list]):
        split_vars = np.array_split(batch_insert_vars, np.ceil(len(batch_insert_vars) / 3000))
        for insert_vars in split_vars:
            res = self.insert_all(sql, insert_vars.tolist())
            if res is False:
                raise Exception("batch insert failed: {}".format(sql))
        return True
