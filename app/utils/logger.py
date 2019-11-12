# -*- coding: utf-8 -*-
import json
from flask import make_response, jsonify

class Response:

    def __init__(self, status, data=None):
        self.status = status
        if data:
            self.data = data
        
    def output(self):
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
        return response

    def Error(self, msg):
        self.msg = "Error obtained - " + msg
        return self.output()
    
    def Success(self, msg):
        self.msg = "Success - " + msg
        return self.output()

    def Info(self, msg):
        self.msg = "Info - " + msg
        return self.output()
