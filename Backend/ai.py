import logging
import os
from typing import Any

import requests

from Backend.db import query_all, query_one

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = "gpt-4o-mini"

logger = logging.getLogger("flower_shop.ai")


def load_knowledge_chunks() -> list[dict[str, str]]:
    rows = query_all("SELECT title, content FROM support_articles ORDER BY id")
    return [{"title": row["title"], "content": row["content"]} for row in rows]


def rag_search(question: str) -> dict[str, Any]:
    chunks = load_knowledge_chunks()
    if not chunks:
        return {
            "answer": "I don't have enough Flower Shop knowledge to answer this question.",
            "source": "rag",
            "confidence": 0.0,
        }

    matched = [chunk for chunk in chunks if question.lower() in chunk["content"].lower() or question.lower() in chunk["title"].lower()]
    if not matched:
        matched = chunks[:2]

    prompt = (
        "Use the following Flower Shop information to answer the question. "
        "Only use the facts from the content and do not invent information.\n\n"
        + "\n\n".join([f"Title: {item['title']}\nContent: {item['content']}" for item in matched])
        + f"\n\nQuestion: {question}"
    )

    if not OPENROUTER_API_KEY:
        logger.warning("OPENROUTER_API_KEY is not configured. Returning grounded stub answer.")
        return {
            "answer": "Based on Flower Shop data, I can say that care instructions and delivery guidance are available.",
            "source": "rag",
            "confidence": 0.6,
        }

    response = requests.post(
        "https://api.openrouter.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful florist assistant. Answer using only the provided Flower Shop information."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 300,
        },
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()
    answer = result["choices"][0]["message"]["content"].strip()
    return {"answer": answer, "source": "rag", "confidence": 0.8}


def count_low_stock(threshold: int = 5) -> dict[str, Any]:
    rows = query_all("SELECT name, stock FROM flowers WHERE stock <= ? ORDER BY stock ASC", (threshold,))
    if not rows:
        return {"answer": "All flowers have healthy stock levels.", "source": "text2sql", "confidence": 0.9}
    items = ", ".join([f"{row['name']} ({row['stock']})" for row in rows])
    return {"answer": f"Flowers with low stock: {items}", "source": "text2sql", "confidence": 0.9}


def find_promotions() -> dict[str, Any]:
    rows = query_all("SELECT code, description FROM promotions WHERE active = 1")
    if not rows:
        return {"answer": "There are no active promotions right now.", "source": "text2sql", "confidence": 0.9}
    items = "; ".join([f"{row['code']}: {row['description']}" for row in rows])
    return {"answer": f"Active promotions: {items}", "source": "text2sql", "confidence": 0.9}
