#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from fastapi.routing import APIRouter
from fastapi import Request, Form
from models.cache import Cache
from helpers.utils import is_empty
from config.constants import CacheKey

router = APIRouter()


@router.post("/events")
async def slack_events(request: Request):
    payload = await request.json()
    print(payload)
    if "challenge" in payload:
        return {"challenge": payload["challenge"]}

    response = {"ok": True}
    if "event" not in payload:
        return response

    event = payload["event"]
    if "subtype" in event and event["subtype"] == "channel_join":
        cache = Cache()
        cache.set_channel_info(event["channel"])
        return response
    if "message" != event["type"]:
        return response
    if "subtype" in event and event["subtype"] != "file_share":
        return response
    if str(event["text"]).startswith("/"):
        return response
    if "bot_profile" in event:
        return response
    if "bot_id" in event:
        return response
    slack_bot_user_id = os.getenv("SLACK_BOT_USER_ID")
    if slack_bot_user_id and event["user"] == slack_bot_user_id:
        return response

    cache = Cache()
    chat_id = event["channel"]
    message_id = event["client_msg_id"]
    channel_id_key = cache.get_message_id_key(message_id)
    if not is_empty(cache.get(channel_id_key)):
        return response

    cache.set(channel_id_key, channel_id_key)

    worker_message = {
        "chat_id": chat_id,
        "ts": event["ts"],
        "text": event["text"],
        "user_id": event["user"],
    }
    # thread 댓글
    if "thread_ts" in event:
        worker_message["thread_ts"] = event["thread_ts"]

    cache.lpush(CacheKey.WORKER_PUSH, worker_message)

    return response


@router.post("/command")
async def slack_command(
    channel_id: str = Form(...),
    channel_name: str = Form(...),
    command: str = Form(...),
    text: str = Form(""),
):
    """
    Slack Slash Command를 처리하는 엔드포인트
    """
    response = {"response_type": "in_channel", "text": "잘못된 명령어 입력입니다."}
    match (command):
        case "/locale":
            language_code = text.upper()
            if language_code not in ["JP", "EN", "ZH"]:
                return response
            country_name = None
            match (language_code):
                case "JP":
                    country_name = "일본어"
                case "EN":
                    country_name = "영어"
                case "ZH":
                    country_name = "중국어"

            cache = Cache()
            cache.update_channel_info(channel_id, channel_name, language_code)
            return {
                "response_type": "in_channel",
                "text": f"채널의 번역 대상이 {country_name}({language_code})로 설정되었습니다.",
            }
        case _:
            return response
