from collections import namedtuple
from flask_restful import Resource
from flask import jsonify, request
from playhouse.shortcuts import model_to_dict
from ibuk.common import EBookReadSchema, Ebook
import json


Filters = namedtuple('Filters', 'id min_size max_size date_from date_to')


def get_filter_data(request):
    filtering = None
    data = json.loads(request.data)
    if data and 'filters' in data:
        filters = data['filters']
        id = int(filters['id']) if 'id' in filters else None
        max_size = int(filters['max_size']) if 'max_size' in filters else None
        min_size = int(filters['min_size']) if 'min_size' in filters else None
        date_from = filters['date_from'] if 'date_from' in filters else None
        date_to= filters['date_to'] if 'date_to' in filters else None
        filtering = Filters(id=id, max_size=max_size, min_size=min_size, date_from=date_from, date_to=date_to)
    return filtering


class EbooksResource(Resource):
    """
    Manages the API endpoint for ebooks to be listed, created, deleted or modified
    endpoint: /api/v1/ebooks
    """
    def put(self):
        """
        Manages the creation of a new ebook in the database. The ebook comes as part of the data.
        :return:
        """
        pass

    def get(self):
        """
        Manages listing the ebooks. Filtering is performed via URL query parameters.

        :return: json representation of the queryset in the database.
        """
        filters = get_filter_data(request)
        query = Ebook.select()
        if filters:
            if filters.id:
                query = query.where( Ebook.id  == filters.id )
        if not query.count():
            return 404
        
        return {'ebooks': EBookReadSchema(many=True, only=('name','description','filename','size')).dump(query).data}


    def delete(self):
        pass
