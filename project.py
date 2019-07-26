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

# auth = HTTPBasicAuth()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
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
    return render_template('home.html')
 
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
                    flash('thanks for registering. Please login') # flashing a successful message
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

    # diplay if the request is  get
    return render_template('login.html')

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
@login_required
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
def createItem(categoryName):
    # if the request is a POST
    if request.method == 'POST':
        # storing the form values
        itemName = request.form['name']
        itemDescription = request.form['description']

        # fetching all the items from the db
        allItems = session.query(Items).all()
        # fetching one category from the db
        cat = session.query(Category).filter_by(name=categoryName).one()

        # looping through all the categories
        for i in allItems:
            # if the object (i) was empty
            if i is None:
                return render_template('newItem.html', categoryName=categoryName)
            else:
                # checking if a category is already existing 
                if i.name == itemName:
                    flash('The Item \'{}\' is already existing'.format(i.name))
                    return render_template('newItem.html', categoryName=categoryName)

                # fetching just one user_id from the user table
                # category_id = session.query(Category).filter_by(category_id=categoryName.id).one()
                
                # storing the item_name, item_description and the category_id 
                item = Items(name=itemName, description=itemDescription, category_id=cat.id)
                session.add(item) # adding the query
                session.commit() # executing the query
                flash('new item added') # flashing a successful message

                return redirect(url_for('allItems', categoryName=categoryName)) # redirecting the user

    # render the template if the request was a GET        
    return render_template('newItem.html', categoryName=categoryName)

# specific item route
@app.route('/catalog/<categoryName>/<itemName>', methods = ['GET'])
def viewItem(categoryName,itemName):
    # fetching just one category from the Category DB where the name matches categoryName
    item = session.query(Items).filter_by(name=itemName).one()
    # item = session.query(Items).filter_by(category_id=cat.id)
    return render_template('itemDetails.html', categoryName=categoryName, items=item)

# edit item for a category
@app.route('/catalog/<categoryName>/<int:item_id>/edit', methods = ['GET','POST'])
def editItem(categoryName, item_id):
    return render_template('editItem.html',categoryName=categoryName,item_id=item_id)

# delete an item from a category
@app.route('/catalog/<categoryName>/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(categoryName, item_id):
    return render_template('deleteItem.html',categoryName=categoryName,item_id=item_id)

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)