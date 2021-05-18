from flask import Flask
from flask_restful import Resource, Api

'''
Resource is something api will be working on.

You can always test your api using postman app or curl command.
Example - if you run the following command on terminal

curl http://127.0.0.1:5000/student/Deepak

you will get the following output - 

{"student": "Deepak"}

This is due to GET method in Student class which returns the resource.

You can also make POST request by following command but this method is not allowed
for the requested URL - curl -X POST http://127.0.0.1:5000/student/Deepak

'''

app = Flask(__name__)
api = Api(app)

class Student(Resource):
    def get(self, name):
        return {'student':name}

api.add_resource(Student, '/student/<string:name>')

app.run(port=5000)