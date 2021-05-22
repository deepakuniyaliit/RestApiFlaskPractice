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


    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def post(self,name):
        '''
        store item to the database if it doesn't exists in the databse already
        '''
        if self.find_by_name(name):
            return {'message':"An item with name '{}' already exits.".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {"name":name, "price":request_data['price']}
        try:
            self.insert(item)
        except:
            return {"message":"An error occurred inserting the data"}, 500

        return item, 201


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


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()


    def put(self,name):
        '''
        insert or update item
        '''
        request_data = Item.parser.parse_args()

        item = self.find_by_name(name)
        print(item)
        print(name, request_data['price'])
        updated_item = {'name':name, 'price':request_data['price']}
        print(updated_item)
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"An error occurred updating the data"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"An error occurred updating the data"}, 500
        return updated_item


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