from dotenv import load_dotenv
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(override=True, verbose=True, dotenv_path=dotenv_path)

from openai import OpenAI

open_ai_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=open_ai_key)


class TranslateRole:
    system_role_template = """
    Just show me the results without any hesitation.
    If the sentence is in Japanese, translate it to Korean. If it's in Korean, translate it to Japanese.

    Show results in JSON format with the following keys and types:
    - detected_language_iso_639_1: string
    - translated_text: string
    """


def translate(text: str, target_lang: str):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",  # 또는 "gpt-3.5-turbo"
        messages=[{"role": "system", "content": TranslateRole.system_role_template}, {"role": "user", "content": text}],
    )

    import json

    response = json.loads(response.choices[0].message.content.strip())
    print(response["detected_language_iso_639_1"])
    print(response["translated_text"])


translate("こんにちは", "JP")
