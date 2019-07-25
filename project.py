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
    # fetching all the category from the database
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('home.html', categories=categories)

# catalog homepage route
@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html')
 
# new user creation route
@app.route('/user/register', methods = ['GET','POST'])
def register():
    # checking if the request was a post
    if request.method == 'POST':
        # fetching the data from the form and storing in variables
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # checking if the username and password is not inputted
        if username is None or password is None:
            flash('A username and password is required')
            abort(400) # missing arguments

        # checking if an email already exist
        if session.query(User).filter_by(email = email).first() is not None:
            flash('username is already existing')
            abort(400) # existing user
        # storing the User data to an object 
        user = User(username = username, email = email, password=password)
        session.add(user)
        session.commit()
        flash('thanks for registering')
        return redirect(url_for('login'))

    # render if the request was a GET
    return render_template('register.html')

# user login route
@app.route('/user/login', methods = ['GET','POST'])
def login():

    # check if the request made is a post
    if request.method == 'POST':
        username = request.form['username']
        u_password = request.form['password']

        # is username and password not present
        if username and u_password is None:
            flash("username and password are required")
            abort(404)
        else:
            # retrieve the username
            user = session.query(User).filter_by(username=username).first()
            
            # verifying the user password
            if user.verify_password(u_password) and user is not '':
                
                login_user(user) # login the user
                flash('login successfully')

                # saving the requested page as next
                next = request.args.get('next')

                # if the request is none
                if next == None or not next[0] == '/':
                    next = url_for('categories')
                return redirect(next) # redirecting to the prevoius or next url
            flash("invalid username or password")
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
        categoryName = request.form['name']
        
        # fetching all the categories from the db
        allCategoryNames = session.query(Category).all()

        # looping through all the categories
        for cat in allCategoryNames:
            # checking if a category is already existing 
            if cat.name == categoryName:
                flash('Sorry \'{}\' category is already existing'.format(cat.name))
                return render_template('newCategory.html')
            
            # fetching just one user_id from the user table
            user_id = session.query(User).filter_by(id=user_id).one()

            # storing the category name and the user_id 
            category = Category(name=categoryName, user_id=user_id.id)
            session.add(category) # adding the query
            session.commit() # executing the query
            flash('new category added') # flashing a successful message
            return redirect(url_for('categories.html', categories=category)) # redirecting the user
 
    # return the template if the request was a GET 
    return render_template('newCategory.html')

# edit a category
@app.route('/catalog/<categoryName>/edit', methods = ['GET','POST'])
def editCategory(categoryName):
    return render_template('editCategory.html',categoryName=categoryName)

# delete a category
@app.route('/catalog/<categoryName>/delete', methods = ['GET','POST'])
def deleteCategory(categoryName):
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