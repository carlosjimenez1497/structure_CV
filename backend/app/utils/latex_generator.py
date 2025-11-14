from typing import List, Optional
from app.models.cv_models import Section

def _esc(s: str) -> str:
    """
    Minimal escaping for LaTeX special characters.
    """
    if not s:
        return ""
    return (
        s.replace("\\", r"\\")
         .replace("&", r"\&")
         .replace("%", r"\%")
         .replace("_", r"\_")
         .replace("#", r"\#")
         .replace("{", r"\{")
         .replace("}", r"\}")
    )


def make_cv_latex(*, name: str, title: Optional[str], skills: List[str], sections: List[Section]) -> str:
    """
    Generate a full LaTeX CV document.
    Fully escaped and compliant with LaTeX.
    """

    skills_line = ", ".join(_esc(skill) for skill in skills)

    # Build all section blocks
    sec_blocks = []
    for s in sections:
        sec_blocks.append(
            "\\section*{" + _esc(s.title) + "}\n"
            "\\begin{itemize}\n"
            f"{_markdown_to_items(s.body_md)}\n"
            "\\end{itemize}\n"
        )

    # Use normal triple-quoted string (NOT raw), escape LaTeX manually
    latex = (
f"""\\documentclass[11pt,a4paper]{{article}}
\\usepackage[margin=1.7cm]{{geometry}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{enumitem}}
\\setlist[itemize]{{left=0pt,label=--,topsep=2pt,itemsep=2pt}}

\\begin{document}

\\begin{center}
{{\\LARGE \\textbf{{{_esc(name)}}}}}\\\\[4pt]
{{\\large {_esc(title or "")}}}
\\end{center}

\\section*{{Skills}}
{skills_line}

{''.join(sec_blocks)}
\\end{{document}}
"""
    )

    return latex


def _markdown_to_items(md: str) -> str:
    """
    Convert simple markdown bullets to LaTeX \item lines.
    """

    if not md:
        return ""

    lines = []
    for line in md.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if stripped:
            lines.append("\\item " + _esc(stripped))

    return "\n".join(lines)
