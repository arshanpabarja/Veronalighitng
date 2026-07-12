import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import TRANSLATION_PROMPT

load_dotenv()

client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def translate_product(data):

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": TRANSLATION_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(data, ensure_ascii=False),
            },
        ],
    )

    return json.loads(response.output_text)