#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from dotenv import load_dotenv
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(override=True, verbose=True, dotenv_path=dotenv_path)

bot_token = os.getenv("SLACK_BOT_TOKEN")

# auth.test API 호출
url = "https://slack.com/api/auth.test"
headers = {
    "Authorization": f"Bearer {bot_token}",
}
response = requests.get(url, headers=headers, timeout=10)

# 응답 출력
if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        print(f"Bot User ID: {data['user_id']}")
    else:
        print(f"Error: {data['error']}")
else:
    print("API 호출 실패")
