from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

todos  = {
    1: {'task': 'write hello world program', 'summary': 'write the code using python'},
    2: {'task': 'write hello world program', 'summary': 'write the code using javascript'},
    3: {'task': 'write hello world program', 'summary': 'write the code using java'},
    4: {'task': 'write hello world program', 'summary': 'write the code using c'},
    5: {'task': 'write hello world program', 'summary': 'write the code using c++'},

}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required', required=True)

class TodosList(Resource):
    def get(self):
        return todos
    
    def post(self):
        args = task_post_args.parse_args()
        todo_id = int(max(todos.keys())) + 1
        todos[todo_id] = {
            'task': args['task'],
            'summary': args['summary']
        }
        return todos[todo_id], 201

class ToDo(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    
    

api.add_resource(ToDo,  '/todos/<int:todo_id>')
api.add_resource(TodosList, '/todos')


if __name__ == '__main__':
    app.run(debug=True)
