from flask import Flask, request
from flask_restful import Resource, Api

'''
In this tutorial we will be implementing CRUD operations using REST Api.
The methods that we are going to use here are - GET, POST, PUT and DELETE

Here we will be taking an example of Item and will perform following operations on it - 
1. GET (get a list of items) /items
2. GET (return a specific item, uniquely identified by its name. No two items may have the same name) /item/<string:name>
3. POST (This will create a new item. If the item already exists, it will fail.) /item/<string:name>
4. PUT (This will create a new item or update an existing item.) /item/<string:name>
5. DELETE (This will delete an item, uniquely identified by it's name) /item/<string:name>

Following HTTP status codes are necessary for this tutorial - 

200 - OK
201 - The request has succeeded and has led to the creation of a resource
202 - The request has been accepted for processing, but the processing has not been completed; in fact, processing may not have started yet.
400 - Bad Request 
404 - Not Found
'''

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        '''
        for item in items:
            if item['name'] == name:
                return item
        '''
        '''
        We can use filter function alternatively.
        Filter returns an iterator yielding those items of iterable for which function(item) is true.
        If function is None, return the items that are true.

        next will return first item found by filter function, if item is not found, will return None.
        '''
        item = next(filter(lambda x:x['name'] == name, items), None)
        
        return {"item":item}, 200 if item else 404
    

    def post(self,name):
        '''
        force=True indicates that we don't need content-Type header.
        It will automatically format the content even if it's not set to
        application/json.

        silent=True Doesn't give any error and returns None
        '''
        if next(filter(lambda x:x['name'] == name, items), None) is not None:
            return {"message":"An item with name '{}' already exists.".format(name)}, 400
            
        request_data = request.get_json(silent=True)
        item = {"name":name, "price":request_data['price']}
        items.append(item)
        return item, 201 


class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)