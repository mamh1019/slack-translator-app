#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import json
import os
from slack_sdk import WebClient
from openai import OpenAI
from helpers.utils import is_empty
from libs.logger import Logger


class SlackTranslatorWorker:
    def __init__(self):
        redis_host = os.getenv("REDIS_HOST")
        redis_port = os.getenv("REDIS_PORT")
        redis_db = os.getenv("REDIS_DB")
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

        open_ai_key = os.getenv("OPENAI_API_KEY")
        self.openai = OpenAI(api_key=open_ai_key)

        slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
        slack_bot_user_id = os.getenv("SLACK_BOT_USER_ID")
        self.client = WebClient(token=slack_bot_token)
        self.bot_user_id = slack_bot_user_id or ""

        self._channel_info_prefix = "slack_translator_channel_info"

    def _get_channel_info(self, channel_id: str):
        key = f"{self._channel_info_prefix}_{channel_id}"
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def openai_translate(self, text: str, target_lang: str):
        target_language_name = None
        match (target_lang.upper()):
            case "KO":
                target_language_name = "Korean"
            case "EN":
                target_language_name = "English"
            case "JP":
                target_language_name = "Japanese"
            case "ZH":
                target_language_name = "Chinese"
            case _:
                return None

        system_role_template = f"""
            Translate the provided sentence as literally as possible, without adding interpretation or paraphrasing. 
            If the sentence is in {target_language_name}, translate it to Korean. If it's in Korean, translate it to {target_language_name}.
            Ensure that the translation stays in the target language and doesn't change the target language name or any proper nouns.
            When encountering English words or technical terms like "server", leave them unchanged and do not translate them.

            For example, if the sentence is "우리는 server 의 상태 값을 알고 싶습니다.", the word "server" should remain untranslated, resulting in:
            "私たちは server の状態を知りたいです。"


            Show results in JSON format with the following keys and types:
            - detected_language_iso_639_1: string
            - translated_language_iso_639_1: string
            - translated_text: string
        """

        try:
            response = self.openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": system_role_template}, {"role": "user", "content": text}],
            )
            return json.loads(response.choices[0].message.content.strip())
        except Exception as e:
            Logger.log("error", e)
            return None

    def run(self):
        while True:
            _, payload = self.redis_client.brpop("slack_translator_worker_push")
            payload = json.loads(payload)

            chat_id = payload["chat_id"]
            ts = payload["ts"]
            text = payload["text"]
            user_id = payload["user_id"]

            channel_info = self._get_channel_info(chat_id)
            if is_empty(channel_info):
                Logger.log("info", "empty channel")
                continue

            target_lang = channel_info["target_lang"]
            openai_response = self.openai_translate(text, target_lang)
            if is_empty(openai_response):
                Logger.log("info", "empty translate")
                continue
            if is_empty(openai_response["translated_text"]):
                Logger.log("info", "empty translated_text")
                continue
            if openai_response["detected_language_iso_639_1"] == openai_response["translated_language_iso_639_1"]:
                Logger.log("info", "detected_language_iso_639_1 == translated_language_iso_639_1")
                continue

            detected_language = openai_response["detected_language_iso_639_1"].lower()
            translated_language = openai_response["translated_language_iso_639_1"].lower()
            translated_text = openai_response["translated_text"]
            if len(text) > 35:
                text = text[:35] + "..."
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{translated_text}",
                    },
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "_Original: {} - <@{}>_".format(
                                text.replace("\n", " ").replace("_", " ").replace("*", ""), user_id
                            ),
                        }
                    ],
                },
            ]

            if "thread_ts" not in payload:
                blocks.append(
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"_{detected_language} → {translated_language} - translated by <@{self.bot_user_id}>_" if self.bot_user_id else f"_{detected_language} → {translated_language}_",
                            }
                        ],
                    }
                )

            response = self.client.chat_postMessage(
                channel=chat_id,
                blocks=blocks,
                thread_ts=ts,
            )
            Logger.log("info", response)
