from google import genai
from google.genai import types

from app.config import settings
from app.models.schemas import (
    OutlineResponse,
    StoryResponse,
    PromptRequest
)


_client = None


def get_client():
    global _client

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    if _client is None:
        _client = genai.Client(
            api_key=settings.gemini_api_key
        )

    return _client


def _generate_structured(prompt: str, schema):

    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_text_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return schema.model_validate_json(
        response.text
    )


def generate_outline(req: PromptRequest) -> OutlineResponse:

    prompt = f"""
Create a cohesive 5-panel comic outline.

Story idea: {req.story_prompt}

Main character: {req.character_name}

Setting: {req.setting}

Tone: {req.tone}

Art style: {req.art_style}

Return exactly 5 panels.

Each panel must advance the story.

Keep the same character identity and visual continuity
across all panels.

Image prompts must be detailed enough for a text-to-image
model and must not contain dialogue text.
"""

    return _generate_structured(
        prompt,
        OutlineResponse
    )


def generate_story(
    req: PromptRequest,
    outline: OutlineResponse
) -> StoryResponse:

    outline_text = outline.model_dump_json(
        indent=2
    )

    prompt = f"""
Expand this 5-panel outline into a polished comic script.

Character: {req.character_name}

Setting: {req.setting}

Tone: {req.tone}

Art style: {req.art_style}

Original story idea: {req.story_prompt}

Outline:

{outline_text}

For every panel provide:

- title
- scene description
- short ambient caption
- narration
- natural character dialogue
- improved image prompt

Preserve panel order and continuity.

Keep dialogue concise enough to fit a comic panel.

Do not put dialogue inside the image prompt.
"""

    return _generate_structured(
        prompt,
        StoryResponse
    )


def generate_story_fallback(
    req: PromptRequest
) -> StoryResponse:

    outline = generate_outline(req)

    return generate_story(
        req,
        outline
    )