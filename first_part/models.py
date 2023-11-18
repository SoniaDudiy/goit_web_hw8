"""
Створіть хмарну базу даних Atlas MongoDB

За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
Під час зберігання цитат (quotes), поле автора в документі повинно бути не рядковим значенням,
а Reference fields полем, де зберігається ObjectID з колекції authors.
"""

from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db="hw", host="mongodb://localhost:27017")


class Authors(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quotes(Document):
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)