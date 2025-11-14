import json
import time
from typing import Any, Dict, List, Optional
from openai import OpenAI
from app.core.config import settings

_client = OpenAI(api_key=settings.OPENAI_API_KEY)

class OpenAIClient:
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.OPENAI_MODEL

    def chat_json(self, messages: List[Dict[str, str]], temperature: Optional[float] = None,
                  max_tokens: Optional[int] = None, retries: int = 2) -> Dict[str, Any]:
        """
        Ask the model to return strict JSON; we validate/repair once if needed.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.TEMPERATURE,
            "max_tokens": max_tokens if max_tokens is not None else settings.MAX_TOKENS,
            "response_format": {"type": "json_object"},
        }

        last_err = None
        for attempt in range(retries + 1):
            try:
                resp = _client.chat.completions.create(**payload)
                content = resp.choices[0].message.content
                return json.loads(content)
            except Exception as e:
                last_err = e
                time.sleep(0.6 * (attempt + 1))
        raise RuntimeError(f"OpenAI JSON call failed: {last_err}")
