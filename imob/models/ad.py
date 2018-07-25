from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)

import datetime

class Post(Document):
    _id: StringField(required=True)
    code = StringField(required=True)
    title = StringField(required=True)
    price = DecimalField(required=True)
    common_price = DecimalField(required=False)
    url = StringField(required=True)
    lat = StringField(required=True)
    lng = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)
    total_area = DecimalField(required=False)
    util_area = DecimalField(required=False)
    bathrooms = IntField(required=False)
    suites = IntField(required=False)
    age = IntField(required=False)
    parking = IntField(required=False)
    price_changed = IntField(required=True)