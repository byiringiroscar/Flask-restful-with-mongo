from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_mongoengine import MongoEngine
import mongoengine as me


app = Flask(__name__)
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
app.config['MONGODB_SETTINGS'] = {
    "db": "todomodel",
    "host": "localhost",
    "port": 27017,
}
api = Api(app)
db = MongoEngine(app)

class TodoModel(db.Document):
    task = db.StringField(required=True)
    summary = db.StringField(required=True)

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required', required=True)

resource_fields = {
    'id': fields.String,
    'task': fields.String,
    'summary': fields.String
}

class TodosList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        #get all data
        results = TodoModel.objects.all()
        serialized_results = [result for result in results]
        return serialized_results
    @marshal_with(resource_fields)
    def post(self):
        args = task_post_args.parse_args()
        todo = TodoModel(task=args['task'], summary=args['summary']).save()
        return todo, 201


class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        try:
            result = TodoModel.objects.get(id=todo_id)
            return result
        except:
            abort(404, message='Could not find task with that id')

    # @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_post_args.parse_args()
        result = TodoModel.objects.get(id=todo_id)
        if not result:
            abort(404, message='Could not find task with that id')
        result.update(task=args['task'], summary=args['summary'])
        return {
            'message': 'Task updated successfully'
        }, 200
    
    def delete(self, todo_id):
        result = TodoModel.objects.get(id=todo_id)
        if not result:
            abort(404, message='Could not find task with that id')
        result.delete()
        return {
            'message': 'Task Deleted successfully'
        }, 200

    

    
    

api.add_resource(ToDo,  '/todos/<string:todo_id>')
api.add_resource(TodosList, '/todos')


if __name__ == '__main__':
    app.run(debug=True)
