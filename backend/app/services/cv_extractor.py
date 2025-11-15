from app.core.openai_client import OpenAIClient

client = OpenAIClient()

SYSTEM_PROMPT = """
You are an expert CV parser. 
You convert messy or formatted CV text into clean structured JSON containing:

- name
- title
- summary
- skills[]
- experience[] with:
    - role
    - company
    - description
    - start_date
    - end_date
- education[] with:
    - degree
    - institution
    - year

Rules:
- Do NOT invent information.
- Only structure what is present.
- Keep dates as YYYY or YYYY-MM.
- Summaries should be factual and concise.
- Always return valid JSON only.
"""

def extract_profile_from_text(cv_text: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Extract structured profile JSON from the following CV text:\n\n{cv_text}"
        }
    ]
    return client.chat_json(messages)
