from flask import Flask, jsonify
import sys
from flask_restful import Api, Resource
from dataclasses import dataclass
from flask_restful import reqparse
from flask_restful import inputs
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'


@dataclass
class Task(db.Model):
    __tablename__ = 'tasks'
    id: int
    event: str
    date: str

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)


db.create_all()

api = Api(app)
parser = reqparse.RequestParser()


class Event(Resource):
    def get(self):
        tasks = Task.query.all()
        return jsonify(tasks)

    def post(self):
        args = parser.parse_args()
        task = Task(event=args['event'], date=args['date'].date())
        db.session.add(task)
        db.session.commit()
        d = {"message": 'The event has been added!', "event": args['event'], "date": str(args['date'].date())}
        return d


class Today(Resource):
    def get(self):
        tasks = Task.query.filter(Task.date == datetime.date.today()).all()
        return jsonify(tasks)


api.add_resource(Event, '/event')
api.add_resource(Today, '/event/today')

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
