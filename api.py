"""
To install the Neopixel library on Raspberry Pi:
curl -L http://coreelec.io/33 | bash

The python script has to run with sudo (can't use the run button in PyCharm)
To make all libraries available they have to be installed with sudo too, for example:
sudo pip install flask_restful
sudo pip install flask
"""

from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

import leds

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')


# prepare data to be sent to the LED strips
def prepare(monitor, top, bottom, left, right, order, inverted):
    colors = []
    for o in range(len(order)):
        if order[o] == 'top':
            if inverted[o]:
                colors += top[::-1]  # Add inverted partial list to final list
            else:
                colors += top
        elif order[o] == 'bottom':
            if inverted[o]:
                colors += bottom[::-1]
            else:
                colors += bottom
        elif order[o] == 'left':
            if inverted[o]:
                colors += left[::-1]
            else:
                colors += left
        elif order[o] == 'right':
            if inverted[o]:
                colors += right[::-1]
            else:
                colors += right
    leds.update(monitor, colors)


class Availability(Resource):
    def get(self):
        return 200


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


api.add_resource(Availability, '/')
api.add_resource(Update, '/update')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    leds.init()

