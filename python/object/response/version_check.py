from pydantic.main import BaseModel

from python.object.response.version import Version


class VersionCheck(BaseModel):
    is_last: bool
    version: Version
