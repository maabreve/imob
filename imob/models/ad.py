from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)

import datetime

class Post(Document):
    _id: StringField(required=True)
    name = StringField(required=True)
    code = StringField(required=True)
    title = StringField(required=True)
    price = StringField(required=True)
    url = StringField(required=True)
    lat = StringField(required=True)
    lng = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)