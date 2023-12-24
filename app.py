from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_mongoengine import MongoEngine


app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    "db": "todomodel",
    "host": "localhost",
    "port": 27017,
}
db = MongoEngine(app)

class TodoModel(db.Document):
    _id = db.IntField(primary_key=True)
    task = db.StringField(required=True)
    summary = db.StringField(required=True)

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required', required=True)

resource_fields = {
    '_id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}

class TodosList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = TodoModel.objects.all()
        return result
    @marshal_with(resource_fields)
    def post(self):
        args = task_post_args.parse_args()
        todo = TodoModel(task=args['task'], summary=args['summary']).save()
        id_ = todo._id
        return {'id': str(id_)}, 201


class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        result = TodoModel.objects.get(_id=todo_id)
        if not result:
            abort(404, message='Could not find task with that id')
        return result
    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_post_args.parse_args()
        result = TodoModel.objects.get(_id=todo_id)
        if not result:
            abort(404, message='Could not find task with that id')
        result.update(task=args['task'], summary=args['summary'])
        return '{} updated '.format(todo_id), 200
    
    def delete(self, todo_id):
        result = TodoModel.objects.get(_id=todo_id)
        if not result:
            abort(404, message='Could not find task with that id')
        result.delete()
        return '{} deleted '.format(todo_id), 200

    

    
    

api.add_resource(ToDo,  '/todos/<int:todo_id>')
api.add_resource(TodosList, '/todos')


if __name__ == '__main__':
    app.run(debug=True)
