from flask_restful import Resource
from flask import jsonify
from playhouse.shortcuts import model_to_dict
from ibuk.common import EBookReadSchema, Ebook
import json


class EbooksResource(Resource):
    """
    Manages the API endpoint for ebooks to be listed, created, deleted or modified
    endpoint: /api/v1/ebooks
    """
    def post(self):
        pass

    def get(self):
        """
        Manages listing the ebooks. Filtering is performed via URL query parameters.

        :return: json representation of the queryset in the database.
        """
        query = Ebook.select()
        return {'ebooks': EBookReadSchema(many=True, only=('name','description','filename','size')).dump(query).data}


    def delete(self):
        pass
