from typing import Dict, List, Optional
from app.core.openai_client import OpenAIClient
from app.models.cv_models import CVInput, CVGenerated, Section
from app.utils.latex_generator import make_cv_latex

SYSTEM_PROMPT = """You are a meticulous CV writer for software/engineering roles.
Return concise, impact-oriented content using metrics and clear structure.
Keep tone professional, no fluff. Prefer bullet points. Output MUST be JSON.
"""

JSON_SCHEMA_HINT = """
Return JSON with keys:
- name (string)
- title (string|null)
- skills (array of strings)
- sections (array of {title, body_md})
- latex (string|null)  // optional: a LaTeX document if requested
"""

def _cv_messages_from_input(cv: CVInput, want_latex: bool) -> List[dict]:
    user_prompt = {
        "objective": "Generate a clean, modern CV from structured input.",
        "latex": want_latex,
        "guidelines": [
            "Use short bullets that start with strong verbs.",
            "Quantify impact where possible (%, #, time saved).",
            "Group content into sections: Summary, Experience, Education, Skills, Projects (optional).",
            "Prefer markdown for section body (body_md).",
            "Avoid personal pronouns and soft skills unless backed by outcomes.",
        ],
        "input": cv.dict(),
        "output_format": JSON_SCHEMA_HINT.strip(),
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": str(user_prompt)}
    ]

def _section_rewrite_messages(section_title: str, current_body_md: str,
                              instructions: str, persona_brief: Optional[dict]) -> List[dict]:
    user_prompt = {
        "task": "Rewrite a single CV section with the same facts, better phrasing.",
        "section_title": section_title,
        "current_body_md": current_body_md,
        "instructions": instructions,
        "persona": persona_brief or {},
        "style": [
            "Concise, metric-driven, ATS-friendly keywords.",
            "No exaggerations; preserve factual accuracy."
        ],
        "output_format": '{"section": {"title": "...", "body_md": "..."}}'
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": str(user_prompt)}
    ]

def _cv_target_messages(profile_dict, job_description: str) -> List[dict]:
    user_prompt = {
        "task": "Rewrite the user's CV to match the job description.",
        "job_description": job_description,
        "profile": profile_dict,
        "instructions": [
            "Preserve factual accuracy, do NOT invent employment.",
            "Expand responsibilities only if consistent with profile.",
            "Highlight achievements and metrics aligned with the job.",
            "Optimize for ATS and relevant keywords.",
            "Return bullet-based markdown for sections.",
        ],
        "output_format": JSON_SCHEMA_HINT.strip()
    }

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": str(user_prompt)}
    ]

class CVService:
    def __init__(self):
        self.client = OpenAIClient()

    async def generate_full_cv(self, cv: CVInput, *, include_latex: bool = False) -> CVGenerated:
        messages = _cv_messages_from_input(cv, include_latex)
        raw = await self.client.chat_json(messages)

        # Fallbacks/normalization
        name = raw.get("name", cv.name)
        title = raw.get("title", cv.title)
        skills = raw.get("skills", cv.skills)
        sections_raw = raw.get("sections", [])
        sections = [Section(**s) for s in sections_raw if "title" in s and "body_md" in s]

        latex = raw.get("latex")
        if include_latex and not latex:
            latex = make_cv_latex(name=name, title=title, skills=skills, sections=sections)

        return CVGenerated(name=name, title=title, skills=skills, sections=sections, latex=latex)

    async def  rewrite_section(self, section_title: str, current_body_md: str,
                        instructions: str, persona_brief: Optional[dict] = None) -> Section:
        messages = _section_rewrite_messages(section_title, current_body_md, instructions, persona_brief)
        raw = await self.client.chat_json(messages)
        section = raw.get("section") or {}
        title = section.get("title", section_title)
        body_md = section.get("body_md", current_body_md)
        return Section(title=title, body_md=body_md)
    
    async def generate_targeted_cv(self, profile: dict, job_description: str,
                             *, include_latex: bool = False) -> CVGenerated:
        """
        Take stored profile (as dict from DB) + job description,
        return an optimized CV version.
        """
        messages = _cv_target_messages(profile, job_description)
        raw = await self.client.chat_json(messages)

        # Normalize
        name = raw.get("name", profile.get("name"))
        title = raw.get("title", profile.get("title"))
        skills = raw.get("skills", profile.get("skills", []))

        sections_raw = raw.get("sections", [])
        sections = [Section(**s) for s in sections_raw if "title" in s and "body_md" in s]

        latex = raw.get("latex")
        if include_latex and not latex:
            latex = make_cv_latex(
                name=name,
                title=title,
                skills=skills,
                sections=sections
            )

        return CVGenerated(
            name=name,
            title=title,
            skills=skills,
            sections=sections,
            latex=latex
        )
