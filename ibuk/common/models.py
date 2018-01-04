from peewee import Model, CharField, IntegerField, DateField
from playhouse.sqlite_ext import SqliteExtDatabase
#from peewee import SqliteDatabase
from ibuk.common.config import Configuration
import datetime


"""
The SQLite database connection
"""
db = SqliteExtDatabase(Configuration.DATABASE_NAME)


def create_tables():
    # Create table for each model if it does not exist.
    # Use the underlying peewee database object instead of the
    # flask-peewee database wrapper:
    print('Creating tables')
    db.create_tables([Ebook], safe=True)


class BaseModel(Model):
    class Meta:
        database = db


class Ebook(BaseModel):
    name = CharField(null=False)
    description = CharField(null=True)
    filename = CharField(null=False)
    path = CharField(null=False)
    uploaded = DateField(null=False, default=datetime.datetime.now())
    uploaded_by = CharField(null=False)
    size = IntegerField(default=0)