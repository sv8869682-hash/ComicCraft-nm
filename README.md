# ComicCraft - AI Comic Story Creator

ComicCraft turns a user prompt into a five-panel comic, generates illustrations, previews the result in a browser, and exports a PDF.

## Architecture
- FastAPI: backend and API routes
- Jinja2: server-rendered frontend
- Gemini: structured outline + story generation
- Gemini image model or Hugging Face: panel illustrations
- Pillow: image handling
- fpdf2: PDF export

The supplied project document originally specifies Gemini Flash/Pro and Stable Diffusion. The code keeps the same workflow but uses the current Google GenAI Python SDK and a configurable image provider. Google's current SDK supports `client.models.generate_content()` and structured Pydantic output; Hugging Face currently supports `InferenceClient.text_to_image()` through Inference Providers. See the official docs before changing models.

## Windows setup
```powershell
cd path\to\comiccraft
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Open `.env` and put your Gemini key in `GEMINI_API_KEY`.

For the easiest first run, keep `IMAGE_PROVIDER=gemini`. If your Gemini account/model does not have image generation access, use `IMAGE_PROVIDER=huggingface` and add `HF_TOKEN`. For UI-only testing without image AI, use `IMAGE_PROVIDER=placeholder`.

Start:
```powershell
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8000/health

## API example
POST `/generate-comic/json`
```json
{
  "story_prompt":"A brave fox exploring an enchanted forest",
  "character_name":"Luna",
  "setting":"Enchanted forest",
  "tone":"Funny",
  "art_style":"Comic book"
}
```

## Important
- Never upload `.env` to GitHub.
- Five-panel generation makes multiple AI calls and can take time.
- PDF export stores files in `static/exports`.
- Generated images are stored in `static/panels`.
