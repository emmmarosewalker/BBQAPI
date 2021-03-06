# BBQAPI
-------------------------------------
PROJECT STRUCTURE WHEN FIRST CREATED
-------------------------------------
```
main_app_folder/
|-- appname.py
|-- config.py
|--- app/
    |------ __init__.py
    |------ models.py
    |------ routes.py
```
-------------------------------------
PROJECT AND DATABASE SETUP
-------------------------------------
1. Create project folder
2. Create venv:
    ```python3 -m venv venv```
3. Activate venv:
    ```source venv/bin/activate```
4. Use pip to install packages:
    ```pip3 install flask
    pip3 install flask-sqlalchemy
    pip3 install flask-migrate
    # import packages in python interactive shell to confirm import successful
    ```
5. Create folders and files as above structure
```
    appname.py :
        Contains just 'from app import app', just acts as main portal to the app
        Make sure to run (venv) $ export FLASK_APP=appname.py so that 'flask run'
        can be used to run the application
    config.py :
        Contains Config class which gets environment variables using os module,
        and has hard-coded fallbacks for development environment. To use in __init__
        use app.config.from_object(Config)
    models.py:
        Imports app instantiated in __init__ and creates classes for database tables.
        See Flask-SQLAlchemy docs for implementation details
    routes.py:
        Creates routes using @app.route('/') flask decorators. Requires app and flask modules
```
6. Setup __init__.py
```
    Imports:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate
    Instantiate flask app, app = Flask(__name__)
    Setup app config
    Instantiate db
    Instantiate Migrate
    Bottom Imports:
        from app import models, routes
```
7. Database
```
    First, set up SQLAlchemy config in config.py
        SQLALCHEMY_DATABASE_URI = ...
        and SQLALCHEMY_TRACK_MODIFICATIONS = False
    Set up models in models.py (don't forget __repr__ methods)
    Using interactive shell to add rows to db:
        >>> from app.models import User
        >>> u = User(username='susan', email='susan@example.com')
        >>> u
        <User susan>
    Create migration repo:
        (venv) $ flask db init
    Run first migration:
        (venv) $ flask db migrate -m "users table"
    Commit first migration:
        (venv) $ flask db upgrade
    Use interactive shell to make changes to db:
    First, import required modules:
        >>> from app import db
        >>> from app.models import User, Post
    Create and commit user:
        >>> u = User(username='john', email='john@example.com')
        >>> db.session.add(u)
        >>> db.session.commit()
    To query the db:
        i. Retrieve all users:
            >>> users = User.query.all()
            >>> users
            [<User john>, <User susan>]
            >>> for u in users:
            ...     print(u.id, u.username)
            ...
            1 john
            2 susan
        ii. Retrieve a user by id:
            >>> u = User.query.get(1)
            >>> u
            <User john>
        iii. Retrieve all users by reverse alphabetical order
            >>> User.query.order_by(User.username.desc()).all()
            [<User susan>, <User john>]
        For more queries see: http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
 ```
8. Make life easier using flask shell
    Rather than having to import modules to test the application, we can use the flask shell
    The purpose of this command is to start a Python interpreter in the context of the application
    To use:
        `(venv) $ flask shell
        >>> app
        <Flask 'app'>`
    To add db instance and models to the flask shell, add this to appname.py:
        ```python
        
        from app import app, db
        from app.models import User, Post

        @app.shell_context_processor
        def make_shell_context():
            return {
                'db': db,
                'User': User,
                'Post': Post
                }
        ```
    Update as required.
    The reason the function returns a dictionary and not a list is that for each item 
    you have to also provide a name under which it will be referenced in the shell, 
    which is given by the dictionary keys.

-------------------------------------
ERROR HANDLING
-------------------------------------
Debug Mode:
    Stop the server
    Set environment variable:
        (venv) $ export FLASK_DEBUG=1
    Restart the server
    Note:
        - Now error messages will be more meaningful. Don't forget to switch out of Debug mode for production
        - If you run flask run while in debug mode, you can then work on your application and any time you 
        save a file, the application will restart to pick up the new code.
```python
#Create debug module:
    #Location:
        #app/errors.py
#Modules required:
    from flask import render_template
    from app import app, db
#Syntax:
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('template_name.html'), 404
 ```
Continue to add for each error code.
**** Note **** for 500 error, which could be a database error, we need to rollback the database
so that any subsequent db accesses are not interfered with. To do this:
    before returning template, add the db rollback method:
    db.session.rollback()

-------------------------------------
ERROR LOGGING WITH EMAIL
-------------------------------------
*** NOTE GMAIL USED FOR SIMPLICITY ***
Own email server should be set up for production, however this is time-consuming and tedious
1. Configure the email settings in Config class:
    ```python
    class Config(object):
    ...
        MAIL_SERVER = os.environ.get('MAIL_SERVER')
        MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
        MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None # allows encrypted connections
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        ADMINS = ['your-email@example.com']
    ```
2. Set up the logging methods in __init__:
    ```python
    Imports (logging module, and SMTPHandler from logging handlers):
    import logging
    from logging.handlers import SMTPHandler

    if not app.debug: # only operate in production mode
        if app.config['MAIL_SERVER']: # only operate if mail server is set up
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_SERVER'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], 
                app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], 
                subject='App server failure',
                credentials=auth, 
                secure=secure)
            mail_handler.setLevel(logging.ERROR) # only report errors, not warnings or debug msgs
            app.logger.addHandler(mail_handler)
     ```

-------------------------------------
BLUEPRINTS
-------------------------------------
In flask, a blueprint is a logical struture that represents a subset 
of the application. A blueprint can include elements such as:
    - routes
    - view functions
    - forms
    - templates 
    - static files
The aim of blueprints is to encapsulate a certain feature of the application. 
The blueprints must be registered with the application. This passes 
all the elements associated with the blueprint to the application. 
You can think of a blueprint as a temporary storage for application 
functionality that helps in organizing your code. 

To create a blueprint:
1. Separate the files associated with the functionality (blueprint) 
    into separate folders, i.e. for error blueprint,
    instead of having all templates together in app/templates/
    you'd have them in app/templates/errors/ and python files 
    in app/errors/ rather than just app/ 
    ** Be sure to change render_template() to use the new sub-directory
2. In the app/errors folder, create an __init__.py file. This will 
    contain the blueprint creation.
    ```python
    from flask import blueprint
    bp = Blueprint('errors', __name__)
    from app.errors import (any python files e.g. handlers)
    ```
    ** The Blueprint class takes the name of the blueprint, the name 
    of the base module (normally __name__) and some optional arguments 
    not included here. 
    ** import modules at the bottom to avoid circular dependencies 
    
3. Finally, register the blueprint with the application:
    in app/__init__.py:
    ```python
    # ... other code here
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    ```


-------------------------------------
THE APPLICATION FACTORY PATTERN
-------------------------------------
Why use this pattern?
    Having the app as a global variable introduces some complications, mainly 
    in the form of limitations for some testing scenarios.
Previously, we needed the app as a global variable in order to use @app 
as a decorator. Now that we have blueprints, we no longer require the global 
variable. 


-------------------------------------
REQUIREMENTS FILE
-------------------------------------
A file containing all the dependencies for your project, so you do not need 
to remember them all. Just run:
    (venv) $ pip freeze > requirements.txt
And the file will automatically be produced.
To install the dependencies:
    (venv) $ pip install -r requirements.txt

-------------------------------------
PRINCIPLES OF REST APIs
-------------------------------------
REST APIs are an architecture originally proposed by Dr. Roy Fielding in his 
doctoral dissertation. He presented six defining characteristics of REST in a
fairly abstract and generic way. Purists argue that REST APIs must encompass all
six principles, however in the industry a more pragmatic approach has been used.

1. Client-Server
    The client-server principle states that in a REST API the roles of the client
    and the server should be clearly differentiated. In practice, this mens that 
    the client and the server are in separate processes that communicate over a 
    transport, which in the majority of cases is the HTTP protocol over a TCP network

2. Layered System
    This principle states that when a client needs to communicate with a server, it 
    may end up connected to an intermediary and not the actual server. That means that 
    for the client, there's no difference in the way it sends requests if not connected 
    directly to the server (and may not even know if it connected to the actual server or
    not).

    Likewise, the server may receive requests via a third-party, and therefore should not 
    assume that the client is always on the other end of the connection. 

    This principle allows for complex architecture through the use of intermediaries 
    such as caches, proxy servers, load balancers, etc.

3. Cache
    Basically, the server is allowed to cache responses to improve system performance. 
    This is indicated through 'cache controls', where the server indicated to
    intermediaries that the response may be cached for future requests. 

    Note that this is rare due to the fact that APIs use encryption, so intermediaries 
    would need to decrypt and re-encrypt responses in order to cache them.

4. Code on Demand
    * Optional requirement. States that the server can provide executable code in 
    responses to the client. It requires an agreement between server and client 
    regarding the kind of executables that will be sent. For that reason, it is 
    rarely used.

5. Stateless
    The stateless principle is one of two core controversies in the REST community, 
    between purists and pragmatists. The stateless principle states that a REST API 
    should not save any client state to be recalled every time a given client sends 
    a request. What this means is that none of the mechanisms that are common in web 
    development to 'remember' users as they navigate the site may be used. 

    In a stateless API, every request needs to include the information that the server 
    needs to identify and authenticate the client and to carry out the request. 

6. Uniform Interface
    This is the most debated principle, and the one most vaguely outlined by Dr. Fielding.
    He enumerated four features of uniform interfaces:
        1. Unique Resource Identifiers (URIs)
        2. Resource Representations
        3. Self-Descriptive Messages
        4. Hypermedia

-------------------------------------
API DESIGN OUTLINE
-------------------------------------

HTTP METHOD        RESOURCE URL         NOTES
___________________________________________________________________
GET                /api/users/<id>      Returns a user
GET                /api/users           Returns a collection of all users
POST               /api/users/<id>      Adds a new user
PUT                /api/users/<id>      Modify a user

```javascript
// JSON Representation of GET to /api/users/<id>
{
    "id":123,
    "username":"john",
    "email":"john@email.com",
    "address":"12 Fake St. Sydney"
}

// JSON Representation of GET to /api/users

{
    "items": [
        {...user...},
        {...user...}
    ],
    "_meta": {
        "total_items": 3
    }
}
```
