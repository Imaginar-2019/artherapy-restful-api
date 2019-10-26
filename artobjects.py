from config import db, app
from models import ArtObject, summary_schema, general_schema
from flask import url_for, abort, send_from_directory
import json
import os
from werkzeug.utils import secure_filename


def _generate_uri_for_object(obj):
    new_obj = {}
    for field in obj:
        if field == 'id':
            new_obj['imageURL'] = url_for('get_artobject_image', id=obj['id'], _external=True)
        new_obj[field] = obj[field]
    return new_obj


def _generate_filename(id):
    return secure_filename(str(id) + '.png')


def _generate_filepath(id):
    filename = _generate_filename(id)
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


def read_all():
    """
    This function responds to a request for /api/artobjects
    with the complete lists of ArtObjects summary info
    :return: json string of list of ArtObjects summary info
    """
    objects = ArtObject.query.all()
    summary = summary_schema.dump(objects)

    return list(map(_generate_uri_for_object, summary))


def send_image(id):
    artobject = ArtObject.query.filter(
        ArtObject.id == id).one_or_none()
    if artobject is None:
        abort(
            404,
            f"ArtObject not found for Id: {id}"
        )

    filename = _generate_filename(id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='image/png')


def upload_image(files):
    print(f'FILES: {files}')

    if 'image' not in files or 'metadata' not in files:
        abort(400, {'error': 'Object cannot be created. There should be metadata and image files'})
    image = files['image']
    if not image:
        abort(400, {'error': 'Object cannot be created. There should be sn image'})

    metadata = json.loads(files['metadata'].read())
    if metadata is None or 'title' not in metadata:
        abort(400, {'error': 'Object cannot be created. There should be title'})

    title = metadata.get("title")
    existing_object = (
        ArtObject.query.filter(ArtObject.title == title).one_or_none()
    )

    if existing_object is None:
        new_object = general_schema.load(metadata, session=db.session)
        db.session.add(new_object)
        db.session.commit()
        data = general_schema.dump(new_object)
        image.save(_generate_filepath(data['id']))
        return data, 201
    else:
        abort(409, f"ArtObject  {title} exists already")
