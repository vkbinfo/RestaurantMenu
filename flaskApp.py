#import curd operations and table name.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#bind our database to a engine that we can perform operation.
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

from flask import Flask,render_template,request,redirect,url_for
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
        return redirect(url_for("RestaurantMenu",restaurant_id=restaurant_id))
    else:
        return render_template("newMenuItem.html",restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit',methods=["GET","POST"])
def editMenuItem(restaurant_id, menu_id):
    if request.method=="POST":
        pass
    else:
        menuObj=session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editMenuItem',restaurant_id=restaurant_id, menuName=menuObj.name)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__=="__main__":
    app.debug=True#you dont to restart server again, if you change something.
    app.run(host='0.0.0.0', port=5000)