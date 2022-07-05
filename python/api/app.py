from uplink import Consumer, json, headers, get, Query
from uplink.returns import json as response
from python.object.response.version_check_response import VersionCheckResponse


class AppGateService(Consumer):

    @response(VersionCheckResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @get("app/checkIfLastDesktopUtility")
    def check_if_last_desktop_utility(self, version: Query("version"), platform: Query("platform")): pass