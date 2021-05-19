'''
REST - The term REST stands for REpresentational State Transfer. It is an architectural style that defines a set of rules in order to create Web Services.
REST is based on the resources which means when we use methods like GET, POST, PUT and DELETE (CRUD operations), we basically create, read, update ond delete a 
resource. To perform these actions we use HTTP methods which are REST API methods.
Whenever a client requests some resource via API, it's made available by server in the form of some light weight data form such as JSON, XML etc.

REST API is based on six principles - stateless, client-server, uniform interface, Cacheable, Layered system, Code on demand.

In this code we are going to use the GET and POST methods to read and write the resources using end points as mentioned below -

GET - server will send data to client
POST - server will receive data from client

POST (create a new store with a given name) - http://127.0.0.1:5000/store {"name":"storeName"}
GET (get a store with a given name) - http://127.0.0.1:5000/store/<string:name> 
GET (return all the stores) - http://127.0.0.1:5000/store
POST (create an item inside a specific store) - http://127.0.0.1:5000/store/<string:name>/item {name:"name", price:xyz}
GET (get all the items from a specific store) - http://127.0.0.1:5000/store/<string:name>/item

'''


from flask import Flask, jsonify, request
from flask.templating import render_template

app = Flask(__name__)

'''
Normally these resources will be stored in a database but we are using a set of data structures
in our case i.e. list and disctionary.
'''
stores = [
    {
        'name':'My Beutiful Store',
        'items':[
            {
                'name':'My Item',
                'price':15.99
            }
        ]

    }
]


@app.route('/')
def home():
    return render_template('index2.html')


# POST /store data:{"name":"storeName"}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /store/<string:name>
@app.route('/store/<string:name>') #127.0.0.1:5000/store/someName
def get_store(name):
    '''
    iterate over stores, if the store name matches, return it.
    If no match, return an error message
    '''
    for store in stores:
        if name == store['name']:
            return jsonify(store)
        else:
            return jsonify({'message':'store not found'})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})


# POST /store/<string:name>/item {name:"name", price:xyz}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
            
    return jsonify({'message':'store not found'})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'store not found'})


'''
Runs the application to local development server
In your system you will see it as 127.0.0.1 or localhost
'''
app.run(port=5000)