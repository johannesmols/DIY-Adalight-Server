from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')


# prepare data to be sent to the LED strips
def prepare(monitor, top, bottom, left, right, order, inverted):
    print('monitor:', monitor, top, bottom, left, right, order, inverted)


# API endpoint to receive color data
class Update(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        monitor = json_data['monitor']
        top = json_data['top']
        bottom = json_data['bottom']
        left = json_data['left']
        right = json_data['right']
        order = json_data['order']
        inverted = json_data['inverted']
        prepare(monitor, top, bottom, left, right, order, inverted)
        return jsonify(json_data)


api.add_resource(Update, '/update')

if __name__ == '__main__':
    app.run(debug=True)
