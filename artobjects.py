from config import db, ALLOWED_EXTENSIONS
from models import ArtObject, summary_schema, coordinate_schema, general_schema, description_schema
from flask import url_for, abort
import json


def _allowed_image_formats(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _generate_uri_for_object(obj):
    new_obj = {}
    for field in obj:
        if field == 'id':
            new_obj['uri'] = url_for('get_object', id=obj['id'], _external=True)
        new_obj[field] = obj[field]
    return new_obj


def read_all():
    """
    This function responds to a request for /api/artobjects
    with the complete lists of ArtObjects summary info
    :return: json string of list of ArtObjects summary info
    """
    objects = ArtObject.query.all()
    summary = summary_schema.dump(objects)

    return list(map(_generate_uri_for_object, summary))


def read_one(id):
    """
    This function responds to a request for /api/artobjects/id
    :param id: id of ArtObject entity
    :return: json string with data of particular ArtObject
    """
    artobject = ArtObject.query.filter(
        ArtObject.id == id).one_or_none()

    if artobject is not None:
        data = coordinate_schema.dump(artobject)
        return data
    else:
        abort(
            404,
            f"ArtObject not found for Id: {id}"
        )


def upload_image(files):
    if 'image' not in files or 'metadata' not in files:
        abort(400, {'error': 'Object cannot be created. There should be metadata and image files'})
    metadata = json.loads(files['metadata'].read())
    if metadata is None or 'title' not in metadata:
        abort(400, {'error': 'Object cannot be created. There should be title'})

    # TODO validate image file

    title = metadata.get("title")
    existing_object = (
        ArtObject.query.filter(ArtObject.title == title).one_or_none()
    )

    if existing_object is None:
        new_object = general_schema.load(metadata, session=db.session)
        db.session.add(new_object)
        db.session.commit()
        data = general_schema.dump(new_object)

        # TODO save image
        return data, 201
    else:
        abort(409, f"ArtObject  {title} exists already")


def create(artobject):
    """
    This function creates a new ArtObject
    based on the passed in object data
    :param artobj: ArtObject to create in ArtObject structure
    :return: 201 on success, 406 on object exists
    """

    if 'title' not in artobject:
        abort(400, {'error': 'Object cannot be created. There should be title'})

    title = artobject.get("title")
    existing_object = (
        ArtObject.query.filter(ArtObject.title == title).one_or_none()
    )

    if existing_object is None:
        new_object = general_schema.load(artobject, session=db.session)
        db.session.add(new_object)
        db.session.commit()
        data = general_schema.dump(new_object)
        return data, 201
    else:
        abort(409, f"ArtObject  {title} exists already")
