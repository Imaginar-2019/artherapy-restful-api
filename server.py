import click
from flask import jsonify, request
from config import app
from artobjects import read_all, create, read_one, upload_image


@app.route('/api/artobjects', methods=['GET'])
def get_objects():
    return jsonify({'artobjects': read_all()})


@app.route('/api/artobjects/body/<int:id>', methods=['GET'])
def get_object(id):
    return jsonify({'artobject': read_one(id)})


@app.route('/api/artobjects', methods=['POST'])
def upload_artobject():
    return jsonify({'artobject': create(request.json)})


@app.route('/api/artobjects/body', methods=['POST'])
def upload_artobject_image():
    return jsonify({'artobject': upload_image(request.files)})


@click.command()
@click.option('--port', default=7777, help='Number of port to listen')
@click.option('--address', default='localhost', help='Server address')
def cli(port, address):
    app.run(debug=True, host=address, port=port)


if __name__ == '__main__':
    cli()
