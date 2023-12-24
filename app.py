from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.String(500), nullable=False)

# with app.app_context():
#     db.create_all()

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required', required=True)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}

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
