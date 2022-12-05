from marshmallow import Schema,fields

class ProfileSerializer(Schema):
     firstname = fields.String()
     lastname = fields.String()
     address = fields.String()
     fullname = fields.String()
     standard=fields.String()
class UserSerializer(Schema):
    id=fields.Integer()
    email=fields.Email()
    phonenumber=fields.String()
    register_number=fields.String()
    address=fields.String()
    fullname=fields.String()
    profile=fields.Nested(ProfileSerializer)