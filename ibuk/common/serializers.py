from marshmallow_peewee import ModelSchema
from ibuk.common import Ebook


class EBookReadSchema(ModelSchema):
    class Meta:
        model = Ebook
        ordered = True
