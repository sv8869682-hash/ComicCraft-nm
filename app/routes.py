from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import TEMPLATES_DIR
from app.models.schemas import PromptRequest
from app.services.gemini_service import generate_outline, generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


def _request_data(
    story_prompt,
    character_name,
    setting,
    tone,
    art_style
):
    return PromptRequest(
        story_prompt=story_prompt.strip(),
        character_name=character_name.strip(),
        setting=setting.strip(),
        tone=tone.strip(),
        art_style=art_style.strip()
    )


def create_comic(req: PromptRequest):
    outline = generate_outline(req)

    story = generate_story(req, outline)

    image_paths = []

    for panel in story.panels:
        image_prompt = (
            f"{panel.image_prompt}. "
            "Comic panel illustration, consistent character design, "
            "no written words, no speech bubbles, no watermark."
        )

        image_paths.append(
            generate_image(
                image_prompt,
                panel.panel_number
            )
        )

    layout = build_comic_layout(
        story,
        image_paths
    )

    pdf_url = save_pdf(
        layout,
        f"{req.character_name}'s Comic"
    )

    return layout, pdf_url


# =========================
# HOME PAGE
# =========================

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================
# GENERATE COMIC
# =========================

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):

    try:

        req = _request_data(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        layout, pdf_url = create_comic(req)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_url": pdf_url,
                "character_name": req.character_name
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "request": request,
                "error": str(exc)
            },
            status_code=500
        )


# =========================
# GENERATE COMIC JSON
# =========================

@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):

    try:

        layout, pdf_url = create_comic(payload)

        return {
            "success": True,
            "message": "Comic generated successfully",
            "layout": layout,
            "pdf_url": pdf_url
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# =========================
# EXPORT SUCCESS
# =========================

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(
    request: Request,
    pdf_url: str = ""
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request,
            "pdf_url": pdf_url
        }
    )


# =========================
# TEST IMAGE
# =========================

@router.get("/test-image")
async def test_image(
    prompt: str = (
        "A brave fox exploring an enchanted forest, "
        "colorful comic book illustration"
    )
):

    try:

        path = generate_image(
            prompt,
            99
        )

        return {
            "success": True,
            "image_url": "/static/panels/panel_99.png",
            "path": path
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )