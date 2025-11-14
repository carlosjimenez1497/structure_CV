from fastapi import APIRouter, HTTPException, Query
from app.models.cv_models import CVInput, CVGenerated, Section
from app.services.cv_service import CVService

router = APIRouter()
svc = CVService()

@router.post("/generate", response_model=CVGenerated)
async def generate_cv(cv_data: CVInput, include_latex: bool = Query(False, description="Also return LaTeX")):
    try:
        return svc.generate_full_cv(cv_data, include_latex=include_latex)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SectionRewriteRequest(Section):
    instructions: str

@router.post("/rewrite-section", response_model=Section)
async def rewrite_section(payload: SectionRewriteRequest):
    try:
        return svc.rewrite_section(
            section_title=payload.title,
            current_body_md=payload.body_md,
            instructions=payload.instructions,
            persona_brief=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
