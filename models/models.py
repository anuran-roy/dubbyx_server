from pydantic import BaseModel
from typing import Optional


class TranslatorData(BaseModel):
    text: str
    source_lang: Optional[str] = "en"
    target_lang: str


class Text2SpeechData(BaseModel):
    text: str
    source_lang: Optional[str] = "en"
    accent: Optional[str] = "US"
    voice: Optional[str] = "f"
