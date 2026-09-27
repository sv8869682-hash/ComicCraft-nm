import base64
import io
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google import genai
from app.config import settings, PANELS_DIR


def _safe_name(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")[:60] or "panel"


def _placeholder(prompt: str, panel_number: int) -> Path:
    img = Image.new("RGB", (1024, 768), (247, 241, 230))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 999, 743), outline=(30, 30, 30), width=6)
    title = f"ComicCraft - Panel {panel_number}"
    draw.text((60, 60), title, fill=(20, 20, 20))
    words = prompt[:280]
    draw.text((60, 130), words, fill=(40, 40, 40), spacing=8)
    path = PANELS_DIR / f"panel_{panel_number}.png"
    img.save(path)
    return path


def _gemini_image(prompt: str, panel_number: int) -> Path:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")
    client = genai.Client(api_key=settings.gemini_api_key)
    interaction = client.interactions.create(
        model=settings.gemini_image_model,
        input=prompt,
    )
    output = getattr(interaction, "output_image", None)
    if output is None or not getattr(output, "data", None):
        raise RuntimeError("Gemini did not return an image.")
    data = base64.b64decode(output.data)
    image = Image.open(io.BytesIO(data)).convert("RGB")
    path = PANELS_DIR / f"panel_{panel_number}.png"
    image.save(path)
    return path


def _huggingface_image(prompt: str, panel_number: int) -> Path:
    if not settings.hf_token:
        raise RuntimeError("HF_TOKEN is missing.")
    from huggingface_hub import InferenceClient
    client = InferenceClient(provider="auto", api_key=settings.hf_token)
    image = client.text_to_image(prompt, model=settings.hf_image_model)
    path = PANELS_DIR / f"panel_{panel_number}.png"
    image.save(path)
    return path


def generate_image(prompt: str, panel_number: int) -> str:
    provider = settings.image_provider.lower()
    if provider == "gemini":
        path = _gemini_image(prompt, panel_number)
    elif provider == "huggingface":
        path = _huggingface_image(prompt, panel_number)
    elif provider == "placeholder":
        path = _placeholder(prompt, panel_number)
    else:
        raise ValueError("IMAGE_PROVIDER must be gemini, huggingface, or placeholder.")
    return str(path)
