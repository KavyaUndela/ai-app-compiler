from pydantic import BaseModel
from typing import Any, Dict, Optional


class PromptRequest(BaseModel):
    prompt: str
    options: Optional[Dict[str, Any]] = None
