from flask import Flask
from flask_restful import Api
from ibuk.api import EbooksResource


__author__ = 'bertothunder@gmail.com'


def add_resources(api):
    api.add_resource(EbooksResource, '/api/v1/ebooks', endpoint='api')


app = Flask(__name__)
api = Api(app)
add_resources(api)