from dotenv import load_dotenv
import os
from slack_sdk import WebClient

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(override=True, verbose=True, dotenv_path=dotenv_path)

bot_token = os.getenv("SLACK_BOT_TOKEN")
bot_user_id = os.getenv("SLACK_BOT_USER_ID", "")
detected_language = "en"
translated_language = "ko"
client = WebClient(token=bot_token)
chat_id = os.getenv("SLACK_TEST_CHANNEL_ID", "C0000000000")
ts = os.getenv("SLACK_TEST_THREAD_TS", "0.0")
origin_text = "안녕하세요."
user_id = os.getenv("SLACK_TEST_USER_ID", "U0000000000")

blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "second",
        },
    },
    {"type": "divider"},
    {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"_Original: {origin_text} - <@{user_id}>_",
            }
        ],
    },
    {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"_{detected_language} → {translated_language} - translated by <@{bot_user_id}>_" if bot_user_id else f"_{detected_language} → {translated_language}_",
            }
        ],
    },
]

response = client.chat_postMessage(
    channel=chat_id,
    blocks=blocks,
    thread_ts=ts,
)
