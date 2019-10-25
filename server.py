import click
from flask import Flask, jsonify, abort, make_response, request

# TODO use database
objects = []
app = Flask(__name__)


@app.route('/api/objects', methods=['GET'])
def get_objects():
    return jsonify({'objects': objects})


@app.route('/api/objects/<int:object_id>', methods=['GET'])
def get_object(object_id):
    obj = list(filter(lambda o: o['id'] == object_id, objects))
    if len(obj) == 0:
        abort(404)
    return jsonify({'object': obj[0]})


@app.route('/api/objects', methods=['POST'])
def create_object():
    print(f'REQUEST: {request}')
    if not request.json or not 'title' in request.json:
        abort(400)

    if len(objects) == 0:
        obj_id = 1
    else:
        obj_id = objects[-1]['id'] + 1
    obj = {
        'id': obj_id,
        'title': request.json['title'],
    }
    objects.append(obj)
    return jsonify({'object': obj}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Object not found'}), 404)


@app.errorhandler(400)
def cannot_be_created(error):
    return make_response(jsonify({'error': 'Object cannot be created'}), 400)


@click.command()
@click.option('--port', default=7777, help='Number of port to listen')
@click.option('--address', default='localhost', help='Server address')
def cli(port, address):
    app.run(debug=True, host=address, port=port)


if __name__ == '__main__':
    cli()
