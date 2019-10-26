import click
from flask import jsonify, request
from config import app
from artobjects import read_all, create, read_one


@app.route('/api/artobjects', methods=['GET'])
def get_objects():
    return jsonify({'artobjects': read_all()})


@app.route('/api/artobjects/body/<int:id>', methods=['GET'])
def get_object(id):
    return jsonify({'artobject': read_one(id)})


@app.route('/api/artobjects', methods=['POST'])
def create_object():
    return jsonify({'artobject': create(request.json)})


@click.command()
@click.option('--port', default=7777, help='Number of port to listen')
@click.option('--address', default='localhost', help='Server address')
def cli(port, address):
    app.run(debug=True, host=address, port=port)


if __name__ == '__main__':
    cli()
