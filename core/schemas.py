from ninja import Schema

class SchemaBase(Schema):
    class Config:
        from_orm = True