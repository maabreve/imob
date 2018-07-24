from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)

import datetime

class Post(Document):
    _id: StringField(required=True)
    name = StringField(required=True)
    code = StringField(required=True)
    title = StringField(required=True)
    price = DecimalField(required=True)
    common_price = DecimalField(required=True)
    url = StringField(required=True)
    lat = StringField(required=True)
    lng = StringField(required=True)
    published = DateTimeField(default=datetime.datetime.now)
    area_total = DecimalField(required=True)
    area_util = DecimalField(required=True)
    banheiros = IntField(required=True)
    suites = IntField(required=True)
    idade = IntField(required=True)
    vagas = IntField(required=True)