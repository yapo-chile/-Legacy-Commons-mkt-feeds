# -*- coding: utf-8 -*-
import domain as d
import datetime
from http import HTTPStatus
from types import MappingProxyType
from flask import make_response, jsonify


class Response():
    def __init__(self, status: int) -> None:
        self.status = status
    
    def toJson(self, msg:d.JSONType, data:d.JSONType=None):
        template = {
            "message": msg
        }
        if data:
            template['message'].update({"data": data})
        template = MappingProxyType(template)
        response = make_response(template['message'], self.status)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] ='*'
        return response
    
    def toCsv(self, stream, filename:str="export"):
        response = make_response(stream.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename={}{}.csv".format(filename, datetime.datetime.now())
        response.headers["Content-type"] = "text/csv"
        return response

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = HTTPStatus(value)
        return self.__status