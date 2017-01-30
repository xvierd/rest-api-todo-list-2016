import datetime

from bson.objectid import ObjectId
from flask import Flask, jsonify, json, Response, request
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from bson.json_util import dumps
from mongoengine import *

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_DB'] = 'todolist'
mongo = MongoEngine(app)


class TodoModel(Document):
    date = mongo.DateTimeField(default=datetime.datetime.now)
    note = mongo.StringField(required=True)
    executed = mongo.BooleanField(default=False, required=True)


@app.route('/')
def hello_world():
    todo = TodoModel(note='Using MongoEngine')
    todo.save()
    return 'Hello World!'


class Todo(Resource):
    def get(self):
        return Response(TodoModel.objects.to_json(), 200, mimetype='application/json')

    def delete(self, todo_id):
        return {'hello': 'world'},

    @staticmethod
    def put():
        TodoModel.objects(id=request.form['_id']).update_one(executed=json.loads(request.form['executed']))
        return 'ok', 200

    @staticmethod
    def post():
        todo = TodoModel(date=datetime.datetime.now(), note=request.form['note'], executed=False)
        todo.save()
        return Response(dumps(todo), 201, mimetype='application/json')


api.add_resource(Todo, '/api/todo')

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
