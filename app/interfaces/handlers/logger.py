# -*- coding: utf-8 -*-
import json
import domain as d
from flask import make_response, jsonify


class Response():
    def __init__(self, status: d.StatusCode, data: d.JSONType = None) -> None:
        self.status = d.ValidateRestStatusCode(status)
        if data:
            self.data = data
    
    def Error(self, msg):
        self.msg = "Error obtained - " + msg
        return self.output()
    
    def Success(self, msg):
        self.msg = "Success - " + msg
        return self.output()

    def Info(self, msg):
        self.msg = "Info - " + msg
        return self.output()

    def output(self) -> d.JSONType:
        template = {
            "body": {
                "message": {"info": self.msg}
            }
        }
        if hasattr(self, 'data'):
            template['body']['message'].update({"data": self.data})
        response = make_response(jsonify(template['body']['message']), self.status)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] ='*'
        return d.JSONType(response)

