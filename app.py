from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

todos  = {
    1: {'task': 'write hello world program', 'summary': 'write the code using python'},
    2: {'task': 'write hello world program', 'summary': 'write the code using javascript'},
    3: {'task': 'write hello world program', 'summary': 'write the code using java'},
    4: {'task': 'write hello world program', 'summary': 'write the code using c'},
    5: {'task': 'write hello world program', 'summary': 'write the code using c++'},

}

class ToDo(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    

api.add_resource(ToDo,  '/todos/<int:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
