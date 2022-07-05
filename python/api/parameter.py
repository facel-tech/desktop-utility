from python.object.response.base_response import BaseResponse
from uplink import Consumer, Body, post, json, headers
from uplink.returns import json as response


class ParameterService(Consumer):

    @response(BaseResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @post("parameter/addDesktopUtility")
    def add_parameter(self, info: Body): pass
