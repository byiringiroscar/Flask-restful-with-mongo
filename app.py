from flask import Flask, jsonify
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
    @marshal_with(resource_fields)
    def get(self):
        result = TodoModel.query.all()
        return result
    @marshal_with(resource_fields)
    def post(self):
        args = task_post_args.parse_args()
        todo = TodoModel(task=args['task'], summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            return jsonify({
                'status': 404,
                'message': 'Not found'
            }), 404
        return result
    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_post_args.parse_args()
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            return jsonify({
                'status': 404,
                'message': 'Not found'
            }), 404
        result.task = args['task']
        result.summary = args['summary']
        db.session.commit()
        return result
    
    def delete(self, todo_id):
        result = TodoModel.query.filter_by(id=todo_id).first()
        if not result:
            return jsonify({
                'status': 404,
                'message': 'Not found'
            }), 404
        db.session.delete(result)
        db.session.commit()
        return '', 204

    

    
    

api.add_resource(ToDo,  '/todos/<int:todo_id>')
api.add_resource(TodosList, '/todos')


if __name__ == '__main__':
    app.run(debug=True)
