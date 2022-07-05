from datetime import datetime

from pydantic import BaseModel

from python.object.response.version_check import VersionCheck


class VersionCheckResponse(BaseModel):
    code: str
    data: VersionCheck
