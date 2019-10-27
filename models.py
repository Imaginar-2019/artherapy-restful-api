from config import db, ma
from marshmallow import fields


class ArtObject(db.Model):
    __tablename__ = 'artobject'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(128))
    coordinate = db.relationship('Coordinate', uselist=False)


class Coordinate(db.Model):
    __tablename__ = 'coordinate'
    artobject_id = db.Column(db.Integer, db.ForeignKey('artobject.id'),
                             nullable=False, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)


class CoordinateSchema(ma.ModelSchema):
    class Meta:
        model = Coordinate
        sqla_session = db.session


class ArtObjectSchema(ma.ModelSchema):
    class Meta:
        model = ArtObject
        sqla_session = db.session
    coordinate = fields.Nested(CoordinateSchema, many=False)


class FeedbackSchema(ma.ModelSchema):
    class Meta:
        model = Feedback
        sqla_session = db.session


general_schema = ArtObjectSchema()
summary_schema = ArtObjectSchema(only=('id', 'title', 'description', 'coordinate'), many=True)
description_schema = ArtObjectSchema(only=('id', 'description',))
coordinate_schema = ArtObjectSchema(only=('id', 'coordinate',))
