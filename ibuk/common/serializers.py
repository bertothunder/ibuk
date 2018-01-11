from marshmallow_peewee import ModelSchema
from marshmallow import post_load
from ibuk.common import Ebook


class EBookReadSchema(ModelSchema):
    class Meta:
        model = Ebook
        ordered = True


class EBookCreateSchema(ModelSchema):
    class Meta:
        model = Ebook
        ordered = True

    @post_load
    def ebook_create(self, data):
        try:
            return Ebook.create(**data)
        except Exception as e:
            print( 'Exception catched for ebook: "{}"'.format(e) )
            return None