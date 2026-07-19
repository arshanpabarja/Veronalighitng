import json
import os

from openai import OpenAI

from .prompts import PROMPT
from .schemas import FamilySEO


client = OpenAI(
    base_url="https://api.gapgpt.app/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def translate_product(data):

    response = client.responses.parse(
        model="gpt-5-mini",
        temperature=0.15,
        text_format=FamilySEO,
        input=[
            {
                "role": "system",
                "content": PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(data, ensure_ascii=False),
            },
        ],
    )

    return response.output_parsed.model_dump()