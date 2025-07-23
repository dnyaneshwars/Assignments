import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key ="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")



async def summarize_text(text: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following research output."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
