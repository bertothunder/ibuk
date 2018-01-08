from collections import namedtuple
from flask_restful import Resource
from flask import jsonify, request
from ibuk.common import EBookReadSchema, Ebook
from operator import attrgetter
import json


def get_filter_data(request):
    filtering = {k:None for k in 'id min_size max_size date_from date_to'.split()}
    if request.data:
        data = json.loads(request.data)
        # Any key not in the list above is just ignored.
        if data and 'filters' in data:
            filters = data['filters']
            for key in filters:
                if key in filtering:
                    filtering[key] = filters[key]
    return filtering


def select_with_filters(filters):
    query = Ebook.select()
    for key in filters:
        if filters[key]:
            query = query.where( attrgetter(key)(Ebook) == filters[key])
    return query



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
        query = select_with_filters(filters)
        if not query.count():
            return 404

        return {'ebooks': EBookReadSchema(many=True, only=('name','description','filename','size')).dump(query).data}


    def delete(self):
        pass
