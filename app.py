import click
from flask import jsonify, request
from config import app
import artobjects
import feedback


@app.route('/api/artobjects', methods=['GET'])
def get_artobjects():
    return jsonify({'artobjects': artobjects.get_all()})


@app.route('/api/artobjects/body/<int:id>', methods=['GET'])
def get_artobject_image(id):
    return {'ID': str(id)}
    # return artobjects.send(id)


@app.route('/api/artobjects', methods=['POST'])
def upload_artobject():
    return jsonify({'artobject': artobjects.upload(request.files)})


@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    return jsonify({'feedback': feedback.get_all()})


@app.route('/api/feedback/body/<int:id>', methods=['GET'])
def get_feedback_image(id):
    return feedback.send(id)


@app.route('/api/feedback', methods=['POST'])
def upload_feedback_img():
    return jsonify({'feedback_img': feedback.upload_image(request.files)})


@click.command()
@click.option('--port', default=5000, help='Number of port to listen')
@click.option('--address', default='localhost', help='Server address')
def cli(port, address):
    if address == 'localhost':
        app.run(threaded=True, port=port)
    else:
        app.run(threaded=True, host=address, port=port)


if __name__ == '__main__':
    cli()
