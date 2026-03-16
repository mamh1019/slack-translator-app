#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class Model:
    _engine: Engine = None

    def __init__(self, db_setting):
        """Create RDBMS Connection via SQLAlchemy Engine"""
        self._engine = create_engine(
            f"mysql+pymysql://{db_setting.db_user}:{db_setting.db_pass}@{db_setting.db_host}/{db_setting.db_name}",
            pool_pre_ping=True,
            pool_recycle=3600,
            future=True,
        )

    @property
    def engine(self) -> Engine:
        return self._engine

    def insert_all(self, sql: str, params: List[Dict[str, Any]]) -> None:
        """Base Query - bulk insert"""
        if not params:
            return
        with self._engine.begin() as conn:
            conn.execute(text(sql), params)

    def commit(self, sql: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Execute write query with transaction"""
        with self._engine.begin() as conn:
            conn.execute(text(sql), params or {})

    def fetchall(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        with self._engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return [dict(row) for row in result.mappings().all()]

    def fetchone(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        with self._engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            row = result.mappings().first()
            return dict(row) if row is not None else None
