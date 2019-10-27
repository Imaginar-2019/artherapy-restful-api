import os
from config import app
from flask import url_for
from werkzeug.utils import secure_filename


def generate_image_uri_for_object(obj, endpoint):
    new_obj = {}
    for field in obj:
        if field == 'id':
            new_obj['imageURL'] = url_for(endpoint, id=obj['id'], _external=True)
        new_obj[field] = obj[field]
    return new_obj


def generate_image_filename(id):
    return secure_filename(str(id) + '.png')


def upload_folder_path(subfolder):
    return os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
