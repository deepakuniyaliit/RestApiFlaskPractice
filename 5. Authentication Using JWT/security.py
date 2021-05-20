'''
In Flask applications we can use either sessions or tokens depending on the 
application we are creating to implement login/logout functionality.

1. Sessions are best suited to applications where you're serving web pages with Flask—i.e. making extensive use of render_template
2. Tokens are best suited to APIs, where your Flask application accepts and returns data to another application (such as mobile apps or web apps).

JWT stands for JSON Web Token, and it is a piece of text with some information encoded into it.
The information stored when doing authentication in a Flask app is usually something that we can use to identify the user for whom we generated the JWT.

Process is as follows - 
1. User provides his username and password
2. We verify the correctness
3. We generate a JWT which contains the user ID
4. We send that to the user
5. Whenever the user makes a request to our application, they must send us the JWT we generated earlier.
By doing this, we can verify the JWT is valid—and then we'll know the user who sent us the JWT is the user for whom we generated it.

Note - 
Since we know the user sent us the JWT that we generated when they logged in, we can treat this used as a "logged in user".
Any user that does not send us a valid JWT, we will treat as a "logged out" user.

Two main libraries for authentication with Flask: Flask-JWT and Flask-JWT-Extended.

Reference - https://pythonhosted.org/Flask-JWT/
'''
from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'Deepak', '123')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

'''
authenticate and identity are required for Flask-JWT to know how to handle an incoming JWT,
and also what data we want to store in an outgoing JWT.
'''
def authenticate(username, password):
    '''
    It accepts username and password, then finds a user matching that username in the database,
    and checks whether password is correct.
    '''
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    '''
    The identity function is used when we receive a JWT (JSON Web Token).
    In any of endpoints (except /auth) the user can send us a JWT alongside their data.
    They will do this by adding a header to their request: Authorization: JWT <JWT_VALUE_HERE>
    Flask-JWT will take the JWT and get the data out of it.
    Data stored inside a JWT is called a "payload", so our identity function accepts that payload as a parameter:
    
    The identity function is not called unless we decorate our endpoints with the @jwt_required() decorator.
    '''
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)