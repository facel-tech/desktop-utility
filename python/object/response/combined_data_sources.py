from pydantic import BaseModel


class CombinedDataSources(BaseModel):
    is_keyboard_enabled: bool