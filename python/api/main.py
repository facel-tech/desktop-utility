from uplink import Consumer, Body, post, json, headers, get, Query
from uplink.returns import json as response
from python.object.response.base_response import BaseResponse
from python.object.response.data_sources_response import DataSourcesResponse
from python.object.response.session_response import SessionResponse


class MainGateService(Consumer):

    @response(BaseResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @post("session/ping")
    def ping_session(self, info: Body): pass

    @response(SessionResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @post("session/start")
    def create_session(self, info: Body): pass

    @response(BaseResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @post("user/setParticularDataSource")
    def set_particular_data_source(self, info: Body): pass

    @response(DataSourcesResponse)
    @json
    @headers({"Content-Type": "application/json"})
    @get("user/getDataSources")
    def get_data_sources(self): pass