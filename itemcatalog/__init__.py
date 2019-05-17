#!usr/bin/env python2.7
# Item Catalog Web Application Server Program
# 2019-05-12
# Author: KYAPCHUNG
from flask import (Flask,
                   render_template,
                   request, redirect,
                   jsonify,
                   url_for,
                   flash,
                   make_response,
                   session as login_session)
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import httplib2
import json
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('/var/www/itemcatalog/itemcatalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


# Connect to Database and create database session
engine = create_engine('postgresql://itemcatalog:udacity@localhost/itemcatalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Main Catalog route
# If a user is logged in, show options to add items
@app.route('/')
@app.route('/catalog')
def showCatalog():
    categories = session.query(Category).order_by(asc(Category.name))
    latest_items = session.query(Item).order_by(desc(Item.id)).limit(9)
    itemTitle = "Latest Items"
    if 'username' not in login_session:
        return render_template('publicCatalog.html', categories=categories,
                               items=latest_items, title=itemTitle)
    else:
        #print login_session
        return render_template('catalog.html', categories=categories,
                               items=latest_items, title=itemTitle)


# Route to show all items available for specified category
@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategoryItems(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    items_category = (session.query(Category)
                      .filter_by(name=category_name).one_or_none())
    items = session.query(Item).filter_by(category_id=items_category.id
                                          ).order_by(desc(Item.id))
    item_count = items.count()
    itemTitle = str(category_name) + " Items (" + str(item_count) + " item(s))"
    if 'username' not in login_session:
        return render_template('publicCatalog.html', categories=categories,
                               items=items, title=itemTitle)
    else:
        return render_template('catalog.html', categories=categories,
                               items=items, title=itemTitle)


# Route to show information for specified item
# If a user is logged in and the creator of the item,
# show options to edit or delete item
@app.route('/catalog/<category_name>/<item_name>')
def showItemInformation(category_name, item_name):
    item_category = (session.query(Category)
                     .filter_by(name=category_name).one_or_none())    
    item = (session.query(Item)
            .filter_by(name=item_name, category_id=item_category.id)
            .one_or_none())
    if 'username' not in login_session:
        return render_template('publicItemDesc.html', item=item)
    if login_session['user_id'] != item.creator:
        return render_template('publicItemDesc.html', item=item)
    else:
        return render_template('itemDesc.html', item=item)


# Route for logged in users to add a new item
@app.route('/catalog/items/new', methods=['GET', 'POST'])
def newItem():
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        item_category = (session.query(Category)
                         .filter_by(name=request.form['category'])
                         .one_or_none())
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_id=item_category.id,
                       creator=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New %s Item: %s Successfully Created'
              % (item_category.name, newItem.name))
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newItem.html', categories=categories)


# Route for logged in users who created the original item
# to edit an existing item
@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    categories = session.query(Category).order_by(asc(Category.name))
    editedItem = session.query(Item).filter_by(name=item_name).one_or_none()
    item_category = (session.query(Category)
                        .filter_by(id=editedItem.category_id)
                        .one_or_none())
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != editedItem.creator:
        return redirect(url_for('showItemInformation',
                                category_name=item_category.name,
                                item_name=editedItem.name))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            new_item_category = (session.query(Category)
                                    .filter_by(name=request.form['category'])
                                    .one_or_none())
            editedItem.category_id = new_item_category.id
        session.add(editedItem)
        session.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('showItemInformation',
                                category_name=new_item_category.name,
                                item_name=editedItem.name))
    else:
        return render_template('editItem.html', categories=categories,
                               item=editedItem)


# Route for logged in users who created the original item to delete an item
@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    itemToDelete = session.query(Item).filter_by(name=item_name).one_or_none()
    item_category = (session.query(Category)
                                    .filter_by(id=itemToDelete.category_id)
                                    .one_or_none())
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != itemToDelete.creator:
        return redirect(url_for('showItemInformation',
                                category_name=itemToDelete.category_name,
                                item_name=itemToDelete.name))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showCategoryItems',
                                category_name=item_category.name))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# JSON API endpoint - view entire catalog
@app.route('/api/v1/catalog')
def showCatalogJSON():
    if request.args.get('key') == app.secret_key:
        catalog_dict = {"Category": []}
        categories = session.query(Category).all()
        for i, category in enumerate(categories):
            items = (session.query(Item)
                     .filter_by(category_id=category.id).all())
            catalog_dict["Category"].append(category.serialize)
            catalog_dict["Category"][i]["Item"] = []

            for j, item in enumerate(items):
                catalog_dict["Category"][i]["Item"].append(item.serialize)
        return json.dumps(catalog_dict)
    else:
        return 'Invalid API Key'


# JSON API endpoint - view all items in a category
@app.route('/api/v1/catalog/<category_name>')
def showCategoryJSON(category_name):
    if request.args.get('key') == app.secret_key:
        output_category = (session.query(Category)
                           .filter_by(name=category_name).one_or_none())
        items = (session.query(Item)
                 .filter_by(category_id=output_category.id).all())
        category_dict = {output_category.name: []}
        category_dict[output_category.name] = [{"Item": []}]
        for j, item in enumerate(items):
            (category_dict[output_category.name][0]["Item"]
             .append(item.serialize))
        return json.dumps(category_dict)
    else:
        return 'Invalid API Key'


# JSON API endpoint - view a specific item
@app.route('/api/v1/catalog/<category_name>/<item_name>')
def showItemJSON(category_name, item_name):
    item_category = (session.query(Category)
                     .filter_by(name=category_name).one_or_none())
    if request.args.get('key') == app.secret_key:
        output_item = (session.query(Item)
                       .filter_by
                       (category_id=item_category.id, name=item_name)
                       .one_or_none())
        item_dict = output_item.serialize
        return json.dumps(item_dict)
    else:
        return 'Invalid API Key'


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, CLIENT_ID=CLIENT_ID)


# Google Login Route
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/itemcatalog/itemcatalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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

    login_session['username'] = data.get('name', '')
    login_session['picture'] = data.get('picture', '')
    login_session['email'] = data['email']

    # See if user exists, if doesn't make new one
    if getUserID(login_session['email']) is None:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    login_session['user_id'] = getUserID(login_session['email'])

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = (session.query(User)
            .filter_by(email=login_session['email']).one_or_none())
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except:
        return None


# Disconnect - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' %
           login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['state']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
