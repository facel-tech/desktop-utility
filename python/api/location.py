from python.object.response.base_response import BaseResponse
from uplink import Consumer, Body, post, json, headers
from uplink.returns import json as response


class LocationService(Consumer):

    @response(BaseResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @post("location/send")
    def add_location(self, info: Body): pass
