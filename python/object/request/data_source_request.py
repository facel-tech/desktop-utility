from pydantic import BaseModel


class SetParticularDataSourceRequest(BaseModel):
    is_keyboard_enabled: bool
