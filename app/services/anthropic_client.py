import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY ="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"
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

HEADERS = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

async def get_claude_research(query: str) -> str:
    payload = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": f"Research on: {query}"}
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(ANTHROPIC_API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()["content"][0]["text"]
