from collections import namedtuple
from flask_restful import Resource
from flask import jsonify, request, make_response
from ibuk.common import EBookReadSchema, EBookCreateSchema, Ebook
from ibuk.api.errors import bad_request
from operator import attrgetter
import json


def get_filter_data(request):
    filtering = {k:None for k in 'id min_size max_size date_from date_to'.split()}
    if request.data:
        data = json.loads(request.data)
        # Any key not in the list above is just ignored.
        # XXX: The problem with the approach below comes from the fact that's too straight: operators are
        # not supported, ranges are not supported, etc. Also, there's no direct relationship between
        # the model's fields and the filters above.
        # This needs to be changed to a filter class with the operators implemented, that should
        # convert the input into proper filters for peewee's query.
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


def process_creation(request):
    ebook_data = json.loads(request.data)
    if not ebook_data or 'e-book' not in ebook_data:
        return bad_request('No e-book data provided')
    data = ebook_data['e-book']
    try:
        ebook, errors = EBookCreateSchema().load(data)
        if errors:
            print(errors)
            return errors, 422
        if not ebook:
            return "Invalid request", 422
        json_ebook = EBookReadSchema().dump(ebook)
        new_location = '/'.join([request.base_url, '/api/v1/uploads/{}'.format(ebook.id)])
        return json_ebook, 200, {'Location': new_location}
    except Exception as e:
        print( "Exception found: {}".format(e) )
        return e, 422


class EbooksResource(Resource):
    """
    Manages the API endpoint for ebooks to be listed, created, deleted or modified
    endpoint: /api/v1/ebooks
    """
    def put(self):
        """
        Process the creation of a new e-book record. The creation process comes in two parts, following
        a resumable upload (used by youtube).

          - one request with the JSON data for the new e-book.
            This generates a response with either error or ok (200), in which case it will attach
            a different URL for uploading the e-book file, via the 'Location' header in the response.
          - The second request for the e-book to be uploaded (to a different resource).
            This second request will be sent to the URL given in the 'Location' header.

          The advantage of this technique comes from both reliability and scalability:
            - it's more reliable as bigger the file being uploaded; the record is already created in the system,
              and the file can be uploaded later.
            - it's more scalable because the url can be sent to a completely different webserver or datacenter,
              CDN, cloud, etc.

        TODO: To ensure existing files are protected and possible security flaw, the endpoint for Location is always
        opened once; when the e-book file is uploaded, the endpoint will be closed.

        :return:
        """
        if not request.data:
            return bad_request('Missing JSON payload of file content')

            return process_creation(request)


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
