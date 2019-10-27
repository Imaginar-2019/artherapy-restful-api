from models import Feedback, FeedbackSchema
from utils import generate_image_uri_for_object, upload_folder_path, generate_image_filename
from flask import abort, send_from_directory
from config import db
import os


IMG_SUBFOLDER = 'feedback'
PARTICULAR_IMG_ENDPOINT = 'get_feedback_image'


def get_all():
    objects = Feedback.query.all()
    summary = FeedbackSchema(many=True).dump(objects)

    return list(map(lambda x: generate_image_uri_for_object(x, PARTICULAR_IMG_ENDPOINT),
                    summary))


def send(id):
    feedback_obj = Feedback.query.filter(
        Feedback.id == id).one_or_none()
    if feedback_obj is None:
        abort(
            404,
            f"Feedback not found for Id: {id}"
        )

    filename = generate_image_filename(id)
    return send_from_directory(upload_folder_path(IMG_SUBFOLDER),
                               filename, mimetype='image/png')


def upload_image(files):
    if 'image' not in files:
        abort(400, {'error': 'Feedback cannot be created. There should be image file'})
    image = files['image']
    new_feedback = Feedback()

    db.session.add(new_feedback)
    db.session.commit()
    data = FeedbackSchema().dump(new_feedback)
    file_path = os.path.join(upload_folder_path(IMG_SUBFOLDER),
                             generate_image_filename(data['id']))
    image.save(file_path)
    return data, 201
