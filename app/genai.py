import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import httpx
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

openai_client = OpenAI(
    api_key="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"
)

anthropic_client = Anthropic(
    api_key="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"
)

router = APIRouter()

# === Prompt Templates ===

sentiment_template = """
You are a sentiment analysis engine. Analyze the **sentiment** of the following text and respond with one of these: Positive, Negative, or Neutral.

Text: "{text}"
Sentiment:
"""

faq_template = """
You are a helpful assistant that answers FAQs clearly and concisely.

Question: "{question}"
Answer:
"""

# === Input Schemas ===

class ResearchInput(BaseModel):
    query: str

class SummaryInput(BaseModel):
    text: str

class SentimentInput(BaseModel):
    text: str

class FAQInput(BaseModel):
    question: str

# === Endpoints ===

@router.post("/research")
async def research_topic(input: ResearchInput):
    try:
        response = anthropic_client.completions.create(
            model="claude-2",
            prompt=f"{HUMAN_PROMPT} Do research and give an in-depth explanation about: {input.query}{AI_PROMPT}",
            max_tokens_to_sample=400
        )
        return {"result": response.completion}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Claude API failed: " + str(e))

@router.post("/summarize")
async def summarize_text(input: SummaryInput):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a summarizer bot."},
                {"role": "user", "content": f"Summarize the following:\n{input.text}"}
            ],
            max_tokens=150
        )
        return {"summary": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

@router.post("/sentiment")
async def analyze_sentiment(input: SentimentInput):
    try:
        prompt = sentiment_template.format(text=input.text)
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        return {"sentiment": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {e}")

@router.post("/faq")
async def answer_faq(input: FAQInput):
    try:
        prompt = faq_template.format(question=input.question)
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return {"answer": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FAQ answering failed: {e}")
