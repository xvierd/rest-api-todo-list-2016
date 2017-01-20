import datetime
from flask import Flask, jsonify, json, Response
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

    def put(self, todo_id):
        return {'hello': 'world'}, 201

    def post(self, new_todo):
        id_todo = mongo.db.todo.insert_one(
            {'date': datetime.datetime.now(), 'note': 'llevar la plata', 'executed': False}).inserted_id
        return Response(dumps(id_todo), 201, mimetype='application/json')


api.add_resource(Todo, '/api/todo')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
