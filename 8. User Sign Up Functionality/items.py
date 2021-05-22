import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field can't be left blank"
    )

    @classmethod
    def find_by_name(cls, name):
        '''
        find item stored in database by name and return it if found
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name':row[0], 'price':row[1]}}


    @jwt_required()
    def get(self, name):
        '''
        retrieve item from the database
        '''
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'item not found'}, 404


    def post(self,name):
        '''
        store item to the database if it doesn't exists in the databse already
        '''
        if self.find_by_name(name):
            return {'message':"An item with name '{}' already exits.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {"name":name, "price":request_data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

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
