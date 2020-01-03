# -*- coding: utf-8 -*-
import domain as d
import datetime
from http import HTTPStatus
from flask import make_response, jsonify, send_file


# Response builds a flask response object depending of its requested type
class Response():
    def __init__(self, status: int) -> None:
        self.status = status

    # toCsv build a response object to be returned as response json object
    def toJson(self, msg: d.JSONType, data: d.JSONType = None):
        template = {
            "message": msg
        }
        if data:
            template['message'].update({"data": data})
        response = make_response(template['message'], self.status)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # toCsv build a response object to be returned as response stream csv
    # object
    def toCsv(self, file, filename):
        response = send_file(file,
                     mimetype='text/csv',
                     attachment_filename=filename,
                     as_attachment=True)
        return response

    # status getter
    @property
    def status(self):
        return self.__status

    # status setter
    @status.setter
    def status(self, value):
        self.__status = HTTPStatus(value)
        return self.__status
