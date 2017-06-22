#import curd operations and table name.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#bind our database to a engine that we can perform operation.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

from flask import Flask,render_template,request,redirect,url_for, flash ,jsonify
app=Flask(__name__)


@app.route('/restaurant/<int:restaurant_id>/')
def RestaurantMenu(restaurant_id):
    resObj=session.query(Restaurant).filter_by(id=restaurant_id).one()
    cursorMenuItem=session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('main.html',restaurant=resObj,items=cursorMenuItem)


# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/newMenu',methods=["GET","POST"])
def newMenuItem(restaurant_id):
    if(request.method=="POST"):
        menuObj=MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(menuObj)
        session.commit()
        flash('Added a MenuItem in MenuTAble')
        return redirect(url_for("RestaurantMenu",restaurant_id=restaurant_id))
    else:
        return render_template("newMenuItem.html",restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=["GET","POST"])
def editMenuItem(restaurant_id, menu_id):
    menuObj = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=="POST":
        menuObj.name=request.form['name']
        session.add(menuObj)
        session.commit()
        flash('EDited menu item')
        return redirect(url_for('RestaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id,menu=menuObj)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete',methods=["GET","POST"])
def deleteMenuItem(restaurant_id, menu_id):
    menuObj = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=="POST":
        session.delete(menuObj)
        session.commit()
        flash('Deleted menu item')
        return redirect(url_for('RestaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',restaurant_id=restaurant_id,item=menuObj)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def menuJsonReturn(restaurant_id):
    cursorMenuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in cursorMenuItem])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def singleMenuJsonReturn(restaurant_id,menu_id):
    cursorMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems=cursorMenuItem.serialize)

@app.route('/')
def MainPage():
    restCursor=session.query(Restaurant).all()
    return render_template('index.html',items=restCursor)

@app.route('/new',methods=["GET","POST"])
def createNewRestaurant():
    if request.method=="POST":
        restObj=Restaurant(name=request.form['name'])
        session.add(restObj)
        session.commit()
        flash("Restaurant Added")
        return redirect(url_for('MainPage'))
    else:
        return render_template('newRestaurant.html')

@app.route('/<int:restaurant_id>/delete', methods=["GET","POST"])
def deleteRestaurant(restaurant_id):
    restObj = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
        cursorMenu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        for menuItem in cursorMenu:
            session.delete(menuItem)
            session.commit()
        session.delete(restObj)
        session.commit()
        flash("Restaurant Deleted")
        return redirect(url_for('MainPage'))
    else:
        return render_template('deleteRestaurant.html', item=restObj,restaurant_id=restaurant_id)

@app.route('/<int:restaurant_id>/edit',methods=["GET","POST"])
def editRestaurantName(restaurant_id):
    restObj=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=="POST":
       restObj.name=request.form["name"]
       session.add(restObj)
       session.commit()
       flash("Edited The restaurant Name")
       return redirect(url_for('MainPage'))
    else:
        return render_template('editRestaurantName.html',item=restObj)

@app.route('/restaurant/JSON')
def restaurantJson():
    cursor_restaurant=session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in cursor_restaurant])


@app.route('/restaurant/<int:restaurant_id>/JSON')
def MenuWhat(restaurant_id):
    cursor_menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in cursor_menu])


if __name__=="__main__":
    app.secret_key = "I_AM_GREAT_AND_I_AM_HAVING_A_GREAT_TIME."
    app.debug=True #you dont to restart server again, if you change something.
    app.run(host='0.0.0.0', port=5000)