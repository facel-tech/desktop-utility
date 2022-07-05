from pydantic import BaseModel


class CombinedDataSource(BaseModel):
    is_camera_enabled: bool
    is_keyboard_enabled: bool
    is_spotify_enabled: bool
    is_slack_enabled: bool
    is_spotify_logged: bool
    is_slack_logged: bool
    is_gmail_logged: bool
