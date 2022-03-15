from flask import Flask
import sys
from flask_restful import Api, Resource
from flask_restful import reqparse
from flask_restful import inputs

app = Flask(__name__)

api = Api(app)
parser = reqparse.RequestParser()


class HelloWorld(Resource):
    def get(self):
        return {"data":"There are no events for today!"}

    def post(self):
        args = parser.parse_args()
        d = {"message": 'The event has been added!', "event": args['event'], "date": str(args['date'].date())}
        return d


api.add_resource(HelloWorld, '/event')

parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)
