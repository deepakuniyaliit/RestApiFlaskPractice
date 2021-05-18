from flask import Flask

app = Flask(__name__)

'''
Every web framework begings with the concept of routes and views. Routes refer to the URL patterns
of an app such as ourapp.com/home, ourapp.com/about and Views refer to the content that will be served at
these URLs. The response could be a web page or API response (data in text form).

@app.route("/") is a python decorator that Flask provides to assign URLs in our app to functions easily.
It means whenever someone visits our app Ex. ourapp.com at a given route, execute home() function

We can handle multiple routes with a single function in the following way - 

@app.route('/')
@app.route('/home')
@app.route('/about')
def home():
    return "Hello World!"

Above code indicates that home() function will be called in case of all three route patterns.
'''
@app.route('/home')
@app.route('/about')
@app.route('/')  #https://google.com/
def home():
    return "Hello, World!"

app.run(port=5000)
