from mongoengine import *


class User(DynamicDocument):
    log_user = StringField(required=True)
    pass_user = StringField(required=True)
    photo = ImageField()
    first_name = StringField()
    last_name = StringField()
    manager = BooleanField()
    korzina = ListField()


class Manga(DynamicDocument):
    name = StringField()
    price = IntField()
    about = StringField()
    photo = ImageField()