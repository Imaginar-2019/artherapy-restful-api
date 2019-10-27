from config import db
from models import ArtObject, summary_schema, general_schema
from flask import abort, send_from_directory
import json
import os
from utils import generate_image_uri_for_object, generate_image_filename, upload_folder_path


IMG_SUBFOLDER = 'artobjects'
PARTICULAR_IMG_ENDPOINT = 'get_artobject_image'


def get_all():
    """
    This function responds to a request for /api/artobjects
    with the complete lists of ArtObjects summary info
    :return: json string of list of ArtObjects summary info
    """
    objects = ArtObject.query.all()
    summary = summary_schema.dump(objects)

    return list(map(lambda x: generate_image_uri_for_object(x, PARTICULAR_IMG_ENDPOINT),
                    summary))


def send(id):
    artobject = ArtObject.query.filter(
        ArtObject.id == id).one_or_none()
    if artobject is None:
        abort(
            404,
            f"ArtObject not found for Id: {id}"
        )

    filename = generate_image_filename(id)
    return send_from_directory(upload_folder_path(IMG_SUBFOLDER),
                               filename, mimetype='image/png')


def upload(files):
    if 'image' not in files or 'metadata' not in files:
        abort(400, {'error': 'Object cannot be created. There should be metadata and image files'})
    image = files['image']
    if not image:
        abort(400, {'error': 'Object cannot be created. There should be an image'})

    metadata = json.loads(files['metadata'].read())
    if metadata is None or 'title' not in metadata:
        abort(400, {'error': 'Object cannot be created. There should be title'})

    new_object = general_schema.load(metadata, session=db.session)
    db.session.add(new_object)
    db.session.commit()
    data = general_schema.dump(new_object)
    file_path = os.path.join(upload_folder_path(IMG_SUBFOLDER),
                             generate_image_filename(data['id']))
    image.save(file_path)
    return data, 201
