#!/usr/bin/python
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash, make_response, abort, g
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)

# login manager object
login_manager = LoginManager()

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Items, Category

# from flask_httpauth import HTTPBasicAuth

from flask import session as login_session
import random
import string

# importing the oauth modules
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# auth = HTTPBasicAuth()

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog App"

app.config['SECRET_KEY'] = 'mysecretkey'

#Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')

# setting the app to make use of login manager 
login_manager.init_app(app)
login_manager.login_view = 'login'

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# catalog homepage route
@app.route('/')
def index():
    categories= session.query(Category).all()
    return render_template('home.html', categories=categories)
 
# new user creation route
@app.route('/user/register', methods = ['GET','POST'])
def register():
    # checking if the request was a post
    if request.method == 'POST':

        # fetching the data from the form and storing in variables
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # is username and password are not empty
        if username and email and password is not '':
            
            # check if an email is not match was False
            if session.query(User).filter_by(email = email).first() is None:

                # check the password length
                if len(password) > 6:

                    # storing the User data to an object 
                    user = User(username = username, email = email, password=password)
                    session.add(user) # adding the object
                    session.commit() # saving the object to the database
                    flash('Thanks for signing up. Please login') # flashing a successful message
                    return redirect(url_for('login')) # redirecting the user

                else:
                    # throw error message if a password length is less than 6
                    flash('Your password must be at least 6 characters')
            else:
                # throw error message if an email already exist
                flash('username is already existing')
        else:  
            # throw this error message if the input fields are empty
            flash('A username, email and password is required')

    # render if the request was a GET
    return render_template('register.html')

# user login route
@app.route('/user/login', methods = ['GET','POST'])
def login():

    # generating a random string + digits as a state
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    # saving that state to an array object
    login_session['state'] = state

    # check if the request made is a post
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # is username and password are inputed
        if username and password is not '':
            
            # retrieve the username and store in an object
            user = session.query(User).filter_by(username=username).first()
            
            # verifying the user password and the user object
            if user.verify_password(password) and user is not '':
                
                login_user(user) # login the user
                # flash('login successfully')

                # saving the requested page as next
                next = request.args.get('next')

                # if the request is none
                if next == None or not next[0] == '/':
                    next = url_for('index')
                return redirect(next) # redirecting to the prevoius or next url
            else:
                # throw error if no match for username or password
                flash("invalid username or password")
        else:
            # throw this error message if the username and password fields are empty
            flash("username and password are required")

    # return if the request is GET and passing the current session state from login_session['state'] object
    return render_template('login.html', STATE=state)

# user logout route
@app.route('/user/logout')
@login_required
def logout():
    logout_user()
    flash("you are logged out")
    return redirect(url_for('index'))

# check for the currently login user
@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        flash('invalid username or password')
        abort(400)  
    return user

# google sign in
@app.route('/oauth/google', methods=['POST'])
def googleConnect():
    # check if request args doesn't match the login_session state
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Parameter'),401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # get the one time code from the server
    code = request.data

    # try to use this one time code for authentication credentials from the server
    try:
        # creating a flow from clients secrets and save in an object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage' # confirm the one time code that our server is sending off
        credentials = oauth_flow.step2_exchange(code) # exchanging the code for credentials
    # if an error occurred during the exchange process
    except FlowExchangeError:
        # making a response object
        response = make_response(json.dumps('Failed to send off the authorization code'), 401)
        # setting the response header
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # validate the access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.come/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
    h = httplib2.Http()
    # storing the response to a result object
    result = json.loads(h.request(url, 'GET')[1])

    # check the result 
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers ['Content-Type'] = 'application/json'

    # verify the actual user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps('Token\'s user ID doesn\'t match with the given user ID'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# create a new category
@app.route('/catalog/category/new/<int:user_id>', methods = ['GET','POST'])
@login_required
def createCategory(user_id):
    # if the request is a post
    if request.method == 'POST':
        # saving the form value 
        inputtedName = request.form['name']
        
        # check if the form was not empty
        if inputtedName is not '':

            # fetching a single category name from the db and storing it in an object
            fetchedCategoryName = session.query(Category).filter_by(name=inputtedName).first()

            # check if object was an empty array
            if fetchedCategoryName is None:
                
                # fetching just the login user_id from the user table
                # user_id = session.query(User).filter_by(id=user_id).one()

                # storing the category name and the user_id 
                category = Category(name=inputtedName, user_id=user_id)
                session.add(category) # adding the query
                session.commit() # executing the query
                flash('new category added') # flashing a successful message
                return redirect(url_for('allCategories', user_id=user_id)) # redirecting the user

            else:
                # check for category name match
                if fetchedCategoryName.name == inputtedName:
                    flash('Sorry \'{}\' category is already existing'.format(inputtedName))
        else:
            flash('a category name is required')

    # return the template if the request was a GET 
    return render_template('newCategory.html')

# catalog homepage route
@app.route('/catalog/categories/<int:user_id>')
def allCategories(user_id):
    category = session.query(Category).filter_by(user_id=user_id)
    return render_template('categories.html', allCats=category)

# edit a category
@app.route('/catalog/<categoryName>/edit', methods = ['GET','POST'])
@login_required
def editCategory(categoryName):

    # if the request is a POST
    if request.method == 'POST':

        # check if the form was not empty
        if request.form['name'] is not '':

            # fetching a single category from the db and storing it in an object
            fetchedCategoryName = session.query(Category).filter_by(name=categoryName).one()

            if fetchedCategoryName.name != request.form['name']:
                # to fix 
                fetchedCategory = session.query(Category).filter_by(id=fetchedCategoryName.id).one()

                # check if object name didn't match the form input name 
                if fetchedCategory.name != request.form['name']:

                    # assign the new name to fetchedCategory
                    fetchedCategory.name = request.form['name']
                    session.add(fetchedCategory) # saving the new category name
                    session.commit()
                    flash('Category \'{}\' updated to \'{}\''.format(fetchedCategory.name,request.form['name'])) # flashing a successful message
                    return redirect(url_for('allCategories', user_id=fetchedCategory.user_id)) # redirecting the user
            else:
                flash('Sorry \'{}\' category is already existing. Please input another name'.format(request.form['name']))
        else:
            flash('a category name is required')

    # return this is the request was a GET
    return render_template('editCategory.html',categoryName=categoryName)

# delete a category
@app.route('/catalog/<categoryName>/delete', methods = ['GET','POST'])
@login_required
def deleteCategory(categoryName):
    # fetching a single category from the db and storing it in an object
    fetchedCategoryName = session.query(Category).filter_by(name=categoryName).first()
    categoryToDel = session.query(Category).filter_by(id=fetchedCategoryName.id).one()
    if request.method == 'POST':
        session.delete(categoryToDel)
        session.commit()
        flash("Category \'{}\' deleted successfully".format(categoryToDel.name))
        return redirect(url_for('allCategories', user_id=categoryToDel.user_id)) # redirecting the user
    return render_template('deleteCategory.html', categoryName=categoryName)

# all items 
@app.route('/catalog/<categoryName>/items')
def allItems(categoryName):
    cat = session.query(Category).filter_by(name=categoryName).one()
    items = session.query(Items).filter_by(category_id=cat.id)
    return render_template('items.html', categoryName=categoryName, items=items) 

# create a new item for a category
@app.route('/catalog/<categoryName>/item/new', methods = ['GET','POST'])
@login_required
def createItem(categoryName):
    # if the request is a POST
    if request.method == 'POST':

        # storing the form values
        itemName = request.form['name']
        itemDescription = request.form['description']

        # check if the form was not empty
        if itemName and itemDescription is not '':

            # fetching a single category name from the db and storing it in an object
            fetchedCategory = session.query(Category).filter_by(name=categoryName).one()

            # fetching a single item name from the db and storing it in an object
            fetchedItem = session.query(Items).filter_by(name=itemName).first()

            # check if object name doesn't match the form name
            if fetchedItem == None :
                
                # storing the item_name, item_description and the category_id 
                item = Items(name=itemName, description=itemDescription, category_id=fetchedCategory.id)
                session.add(item) # adding the query
                session.commit() # executing the query
                flash('New item added') # flashing a successful message
                return redirect(url_for('allItems', categoryName=categoryName)) # redirecting the user

            else:
                flash('The Item \'{}\' is already existing'.format(fetchedItem.name))
        else:
            flash('an item name and description is required')

    # render the template if the request was a GET        
    return render_template('newItem.html', categoryName=categoryName)

# specific item route
@app.route('/catalog/<categoryName>/<itemName>')
def viewItem(categoryName,itemName):
    # fetching just one category from the Category DB where the name matches categoryName
    item = session.query(Items).filter_by(name=itemName).one()
    return render_template('itemDetails.html', categoryName=categoryName, item=item)

# edit item for a category
@app.route('/catalog/<categoryName>/<itemName>/edit', methods = ['GET','POST'])
@login_required
def editItem(categoryName, itemName):
    # if the request is a POST
    if request.method == 'POST':

        # storing the form values 
        formItemName = request.form['name']
        formItemDescription = request.form['description']
        formItemCategory = request.form['category']

        # check if the form was not empty
        if formItemName and formItemDescription and formItemCategory is not '':

            # fetching a single category from the db and storing it in an object
            fetchedSingleItem = session.query(Items).filter_by(name=itemName).one()
            fetchedCategory = session.query(Category).filter_by(name=formItemCategory).one()

            # check if the form name doesn't match the fetchedSingleItem name
            if fetchedSingleItem.name != formItemName:

                # fetching the id of the fetchedSingleItem
                fetchedItem = session.query(Items).filter_by(id=fetchedSingleItem.id).one()
                # fetching the id of the category
                fetchedCategoryId = session.query(Category).filter_by(id=fetchedCategory.id).one()

                # check if the object isn't empty
                if fetchedItem is not '':
                    # assign the new name to fetchedItem
                    fetchedItem.name = formItemName
                    fetchedItem.description = formItemDescription 
                    fetchedItem.category_id = fetchedCategoryId.id # updating the category
                    session.add(fetchedItem) # saving the new category name
                    session.commit()
                    flash('Item \'{}\' updated to \'{}\''.format(fetchedSingleItem.name, formItemName)) # flashing a successful message
                    return redirect(url_for('allItems', categoryName=categoryName)) # redirecting the user

            else:
                flash('Sorry an \'{}\' item is already existing. Please input another name'.format(request.form['name']))
        else:
            flash('an item name, description and category name is required')

    # return if the request was a GET
    return render_template('editItem.html', categoryName=categoryName,itemName=itemName)

# delete an item from a category
@app.route('/catalog/<categoryName>/<itemName>/delete', methods = ['GET','POST'])
@login_required
def deleteItem(categoryName, itemName):
    # fetching a single item from the db and storing it in an object
    fetchedItem = session.query(Items).filter_by(name=itemName).one()
    # fetching the item id
    itemToDel = session.query(Items).filter_by(id=fetchedItem.id).one()

    # check if the request was a POST
    if request.method == 'POST':
        session.delete(itemToDel) # staging the item to delete
        session.commit() # commiting the query
        flash("Item \'{}\' deleted successfully".format(itemToDel.name))
        return redirect(url_for('allItems', categoryName=categoryName)) 
    
    # return this template if the request was a GET
    return render_template('deleteItem.html',categoryName=categoryName,item=fetchedItem)

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)