from pydantic import BaseModel

from python.object.update import Update


class ConfidentialUserUpdateNotification(BaseModel):
    update: Update
    update_type: str
    timestamp: int
