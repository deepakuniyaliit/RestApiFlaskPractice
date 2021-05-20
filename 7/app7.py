from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)

app.secret_key = 'deepak'
api = Api(app)

jwt = JWT(app, authenticate, identity)
items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field can't be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return {"item":item}, 200 if item else 404
    
    def post(self,name):
        if next(filter(lambda x:x['name'] == name, items), None) is not None:
            return {"message":"An item with name '{}' already exists.".format(name)}, 400
        request_data = Item.parser.parse_args()
        item = {"name":name, "price":request_data['price']}
        items.append(item)
        return item, 201 

    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Item deleted'}

    def put(self,name):
        '''
        Request parsing will allow only few arguments of payload while updating the item details.
        Without using it, name of the item will also be updated in the dictionary, which is not required.
        '''
        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price':request_data['price']}
            items.append(item)
        else:
            item.update(request_data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)