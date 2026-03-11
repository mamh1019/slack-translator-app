#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from .slack.controller import router as slack_router

router = APIRouter()
router.include_router(slack_router, prefix="/slack")
