from pydantic import BaseModel


class CreateLanguageRequestSchema(BaseModel):
    lang: str
    slug: str
    interface: bool
    full_audio: bool
    subtitles: bool