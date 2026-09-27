from pydantic import BaseModel, Field
from typing import List

class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str

class OutlineResponse(BaseModel):
    panels: List[PanelOutline] = Field(min_length=5, max_length=5)

class StoryPanel(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str

class StoryResponse(BaseModel):
    panels: List[StoryPanel] = Field(min_length=5, max_length=5)

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(min_length=1, max_length=100)
    setting: str = Field(min_length=1, max_length=200)
    tone: str = Field(min_length=1, max_length=100)
    art_style: str = Field(min_length=1, max_length=100)

class GenerateResponse(BaseModel):
    success: bool
    message: str
    layout: list[dict]
    pdf_url: str
