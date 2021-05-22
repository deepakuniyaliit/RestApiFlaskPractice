from models.item import ItemModel
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field can't be left blank"
    )

    @jwt_required()
    def get(self, name):
        '''
        retrieve item from the database
        '''
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'}, 404

    def post(self,name):
        '''
        store item to the database if it doesn't exists in the databse already
        '''
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exits.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert()
        except:
            return {"message":"An error occurred inserting the data"}, 500
        return item.json(), 201

    def delete(self,name):
        '''
        delete data from database
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'Item deleted'}
        
    def put(self,name):
        '''
        insert or update item
        '''
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        print(updated_item.name, updated_item.price)
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message":"An error occurred updating the data"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message":"An error occurred updating the data"}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        '''
        retrieve every item from the database
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        connection.close()
        return {'items':items}