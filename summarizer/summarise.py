# summarizer/groq_summarizer.py

import os
import time
from functools import lru_cache
from groq import Groq

client = Groq(api_key="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")

@lru_cache(maxsize=128)
def summarize(text: str) -> str:
    if not text.strip():
        return ""

    messages = [
        {
            "role": "system",
            "content": (
                "You are a cybersecurity assistant. "
                "Provide a concise (2–3 sentence) summary of the following threat report:\n\n"
            )
        },
        {"role": "user", "content": text}
    ]

    try:
        start = time.time()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=150,
            temperature=0.2
            # ← request_timeout removed
        )
        duration = time.time() - start
        print(f"🕒 summarize() took {duration:.1f}s for {len(text)} chars")
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"⚠️ summarize() error: {e}")
        # fallback to a cheap truncation
        snippet = text.strip().replace("\n", " ")
        return (snippet[:200].rsplit(" ", 1)[0] + " …") if len(snippet) > 200 else snippet
