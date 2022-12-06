# from .extension import db
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import json
import datetime


from mongoengine import Document, StringField, EmailField, IntField


class User(Document):
    email = EmailField(required=True)
    phone = IntField(required=True)
    # first_name = StringField(max_length=1000)
    # last_name = StringField(max_length=1000)
    # age = IntField()


class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return PydanticObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            type="string",
            examples=["5eb7cf5a86d9755df3a6c593", "5eb7cfb05e32e07750a1756a"],
        )


# ENCODERS_BY_TYPE[PydanticObjectId] = str


class User(BaseModel):
    email: str
    phone: int

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        return data

    def to_json(self):
        return json.dumps(self, cls=JSONEncoder)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        print(self, o)
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)