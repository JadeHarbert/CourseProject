import os

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from wtforms import SelectField, SubmitField, StringField, DecimalField, SelectMultipleField
from wtforms.validators import InputRequired

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'hard to guess string'
dbname = os.environ['DBNAME']
dbhost = os.environ['DBHOST']
dbuser = os.environ['DBUSER']
dbpass = os.environ['DBPASS']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
moment = Moment(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Association table with items and toppings
Menus = db.Table('menu',
                 db.Column('items_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
                 db.Column('toppings_id', db.Integer, db.ForeignKey('toppings.id'), primary_key=True)
                 )


# one to many with items
class Categories(db.Model):
    """
    Class representing the Categories table in the database
    """
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('Items', backref='categories')


# Many to one with categories

# One to many with Menu
class Items(db.Model):
    """
    Class representing the Items table in the database
    """
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    toppings = db.relationship('Toppings',
                               secondary=Menus,
                               backref=db.backref('items'))


# many to many with menu
class Toppings(db.Model):
    """
    Class representing the Toppings table in the database
    """
    __tablename__ = "toppings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


with app.app_context():
    """
    Creates all the tables in the dataset and populates them with data
    """
    db.drop_all()
    db.create_all()

    # Creates all the toppings for the Toppings table
    lettuce_topping = Toppings(name='Lettuce')
    tomato_topping = Toppings(name='Tomato')
    ketchup_topping = Toppings(name='Ketchup')
    mustard_topping = Toppings(name='Mustard')
    onion_topping = Toppings(name='Onion')
    pickle_topping = Toppings(name='Pickle')
    cheese_topping = Toppings(name='Cheese')
    mayo_topping = Toppings(name='Mayonnaise')
    bacon_topping = Toppings(name='Bacon')
    cherry_topping = Toppings(name='Cherry')
    chicken_topping = Toppings(name='Crispy Chicken')
    turkey_topping = Toppings(name='Turkey')
    ham_topping = Toppings(name='Ham')
    mush_topping = Toppings(name='Mushroom')
    greenpep_topping = Toppings(name='Green Peppers')
    steak_topping = Toppings(name='Shaved Steak')
    bananapep_topping = Toppings(name='Banana Peppers')

    # Adds all the toppings to the database
    db.session.add_all([lettuce_topping, tomato_topping, ketchup_topping, mustard_topping,
                        onion_topping, pickle_topping, cheese_topping, mayo_topping, bacon_topping,
                        cherry_topping, chicken_topping, turkey_topping, ham_topping, mush_topping,
                        greenpep_topping, steak_topping, bananapep_topping])

    # Creates all the categories for the categories table
    burger_category = Categories(name='Burger', id=1)
    sandwich_category = Categories(name='Sandwich', id=2)
    salad_category = Categories(name="Salad", id=3)
    appetizer_category = Categories(name="Appetizer", id=4)
    sub_category = Categories(name="Sub", id=5)
    fried_chicken_category = Categories(name='Fried Chicken', id=6)

    # Adds all the categories to the database
    db.session.add_all([burger_category, sandwich_category, salad_category,
                        appetizer_category, sub_category, fried_chicken_category])

    # Creates the cheeseburger item and creates an array for the relevant toppings
    cheeseburger_item = Items(name='Cheeseburger', price='8.99', category_id=burger_category.id)
    cheeseburger_toppings = [cheese_topping, mustard_topping, ketchup_topping, pickle_topping, onion_topping]

    # Adds the toppings to the item
    for topping in cheeseburger_toppings:
        cheeseburger_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    dexter_deluxe_item = Items(name='Dexter Deluxe', price='9.99', category_id=burger_category.id)
    dexter_deluxe_toppings = [cheese_topping, mustard_topping, ketchup_topping, pickle_topping, onion_topping,
                              mayo_topping]

    # Adds the toppings to the item
    for topping in dexter_deluxe_toppings:
        dexter_deluxe_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    bruin_lake_blt_item = Items(name='Bruin Lake BLT', price='12.99', category_id=sandwich_category.id)
    bruin_lake_blt_toppings = [cheese_topping, bacon_topping, mayo_topping, lettuce_topping, tomato_topping]

    # Adds the toppings to the item
    for topping in bruin_lake_blt_toppings:
        bruin_lake_blt_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    yacht_club_item = Items(name='Yacht Club', price='13.99', category_id=sandwich_category.id)
    yacht_club_toppings = [bacon_topping, cheese_topping, lettuce_topping, tomato_topping, mayo_topping,
                           turkey_topping, ham_topping]

    # Adds the toppings to the item
    for topping in yacht_club_toppings:
        yacht_club_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    pure_salad_item = Items(name='Pure Michigan Chicken Salad', price='10.99', category_id=salad_category.id)
    pure_salad_toppings = [lettuce_topping, bacon_topping, tomato_topping, cheese_topping, cherry_topping,
                           chicken_topping]

    # Adds the toppings to the item
    for topping in pure_salad_toppings:
        pure_salad_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    garden_salad_item = Items(name='Garden Salad', price='6.99', category_id=salad_category.id)
    garden_salad_toppings = [lettuce_topping, cheese_topping, tomato_topping, onion_topping]

    # Adds the toppings to the item
    for topping in garden_salad_toppings:
        garden_salad_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    philly_item = Items(name='Philly Cheese Steak', price='13.99', category_id=sub_category.id)
    philly_toppings = [cheese_topping, onion_topping, steak_topping, mush_topping, greenpep_topping]

    # Adds the toppings to the item
    for topping in philly_toppings:
        philly_item.toppings.append(topping)

    # Creates the dexter_deluxe item and creates an array for the relevant toppings
    veggie_item = Items(name='Straight and Arrow Veggie', price='9.99', category_id=sub_category.id)
    veggie_toppings = [onion_topping, greenpep_topping, lettuce_topping, tomato_topping, cheese_topping,
                       bananapep_topping]

    # Adds the toppings to the item
    for topping in veggie_toppings:
        veggie_item.toppings.append(topping)

    # Creates all the appetizer items
    mozz_stick_item = Items(name='Mozzarella Sticks', price='6.99', category_id=appetizer_category.id)
    onion_ring_item = Items(name='Onion Rings', price='6.99', category_id=appetizer_category.id)
    fries_item = Items(name='French Fries', price='3.99', category_id=appetizer_category.id)
    curly_fries_item = Items(name='Curly Fries', price='3.99', category_id=appetizer_category.id)

    # Creates all the fried chicken items
    chicken_leg_item = Items(name='Chicken Leg', price='2.99', category_id=fried_chicken_category.id)
    chicken_wing_item = Items(name='Chicken Wing', price='2.79', category_id=fried_chicken_category.id)
    chicken_thigh_item = Items(name='Chicken Thigh', price='2.99', category_id=fried_chicken_category.id)
    chicken_breast_item = Items(name='Chicken Breast', price='3.69', category_id=fried_chicken_category.id)

    # Adds all the items to the database
    db.session.add_all([cheeseburger_item, dexter_deluxe_item, bruin_lake_blt_item, pure_salad_item, garden_salad_item,
                        philly_item, veggie_item, mozz_stick_item, onion_ring_item, fries_item, curly_fries_item,
                        chicken_breast_item, chicken_thigh_item, chicken_leg_item, chicken_wing_item])
    db.session.commit()


@app.route('/', methods=['GET'])
def index():
    """
    Method that returns index.html for the / URL
    :return: index.html
    """
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    """
    Method that returns about.html for the /about URL
    :return: about.html
    """
    return render_template('about.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    """
    Method that displays the menu on menu.html for the /menu URL
    :return: menu.html
    """
    form = FilterForm()

    # Gets all of the items in the menu and passes them to menu.html
    burger_id = Categories.query.filter_by(name="Burger")[0].id
    burgers = Items.query.filter_by(category_id=burger_id).all()

    sandwich_id = Categories.query.filter_by(name="Sandwich")[0].id
    sandwiches = Items.query.filter_by(category_id=sandwich_id).all()

    salad_id = Categories.query.filter_by(name='Salad')[0].id
    salads = Items.query.filter_by(category_id=salad_id).all()

    sub_id = Categories.query.filter_by(name='Sub')[0].id
    subs = Items.query.filter_by(category_id=sub_id).all()

    app_id = Categories.query.filter_by(name='Appetizer')[0].id
    apps = Items.query.filter_by(category_id=app_id).all()

    chicken_id = Categories.query.filter_by(name='Fried Chicken')[0].id
    chickens = Items.query.filter_by(category_id=chicken_id).all()

    filter_by = 'All'

    # Displays the specific menu items based on the filter
    if form.validate_on_submit():
        filter_by = form.filter.data
        return render_template('menu.html', burgers=burgers, sandwiches=sandwiches, salads=salads, form=form,
                               filter=filter_by, subs=subs, apps=apps, chickens=chickens)

    # Displays all the menu items on first load of webpage
    return render_template('menu.html', burgers=burgers, sandwiches=sandwiches, salads=salads, form=form,
                           filter=filter_by, subs=subs, apps=apps, chickens=chickens)


class FilterForm(FlaskForm):
    """
    Form represnting filtering the menu by category
    """
    filter = SelectField("Filter by:", choices=['All', 'Burgers', 'Sandwiches', "Salads",
                                                "Appetizers", "Subs", "Fried Chicken"])
    submit = SubmitField('Submit')


@app.route('/contact', methods=['GET'])
def contact():
    """
    Method that returns the contact.html for the /contact URL
    :return: contact.html
    """
    return render_template('contact.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Method that returns admin.html for the /admin URL
    Depending on the selection on AdminForm, it returns a redirect for the specified choice
    :return:
    """
    form = AdminForm()
    if form.validate_on_submit():
        if form.change.data == 'Add Item':
            return redirect(url_for('add'))
        elif form.change.data == 'Delete Item':
            return redirect(url_for('delete'))

    return render_template('admin.html', form=form)


@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    """
    Method for returning add.html for /admin/add
    The method is also responsible for getting the categories & toppings and sending them to add.html to be displayed
    :return: add.html
    """
    form = AddItemForm()

    # Gets all the possible categories and sets form.categories.choices to be the that
    categories = Categories.query.all()
    category_names = []
    for category in categories:
        category_names.append(category.name)
    form.categories.choices = category_names

    # Gets all the possible toppings and sets form.toppings.choices to be that
    toppings = Toppings.query.all()
    topping_names = []
    for topping in toppings:
        topping_names.append(topping.name)

    form.toppings.choices = topping_names

    if form.validate_on_submit():
        category = form.categories.data
        toppings = form.toppings.data
        name = form.name.data
        price = form.price.data

        # Creates a new item with the user's input and attempts to add it to the database
        try:
            with app.app_context():
                new_item = Items(name=name, price=price, category_id=Categories.query.filter_by(name=category)[0].id)
                for topping in toppings:
                    new_item.toppings.append(Toppings.query.filter_by(name=topping)[0])
                db.session.add(new_item)
                db.session.commit()
                return render_template('add.html', isSuccessful=True)
        except IntegrityError:
            return render_template('add.html', error="IntegrityError")
        except:
            return render_template('add.html', isSuccessful=False)

    return render_template('add.html', form=form)


@app.route('/admin/delete', methods=['GET', 'POST'])
def delete():
    """
    Method for returning delete.html to /admin/delete
    The method is also responsible for taking in user input for which item they want to delete
    It then deletes that item from the database
    :return: delete.html
    """
    form = DeleteForm()
    item = form.items.data

    # Gets all the items in the database and sets form.items.choices to be that
    items = Items.query.all()
    item_names = []
    for itm in items:
        item_names.append(itm.name)
    form.items.choices = item_names

    if form.validate_on_submit():
        # Attempts to delete the item from the database
        try:
            item_to_delete = Items.query.filter_by(name=item)[0]
            db.session.delete(item_to_delete)
            db.session.commit()
            isSuccessful = True
            return render_template('delete.html', isSuccessful=isSuccessful)
        except:
            isSuccessful = False
            return render_template('delete.html', isSuccessful=isSuccessful)
    return render_template('delete.html', form=form)


class DeleteForm(FlaskForm):
    """
    Form representing items that are able to be deleted
    """
    items = SelectField('Select Item to Delete', validators=[InputRequired()], choices=[])
    submit = SubmitField('Delete Item')


class AdminForm(FlaskForm):
    """
    Form representing the powers an admin has
    """
    change = SelectField("Edit database by:", choices=["Add Item", 'Delete Item'])
    submit = SubmitField('Submit')


class AddItemForm(FlaskForm):
    """
    Form representing the fields for adding an item
    """
    name = StringField("Enter name of item:", validators=[InputRequired()])
    price = DecimalField("Enter price of item:", validators=[InputRequired()])
    categories = SelectField("Select category for item:", choices=[], validators=[InputRequired()])
    toppings = SelectMultipleField("Select Toppings: (CTRL Click for Multiple) ", choices=[])

    submit = SubmitField("Add Item")


if __name__ == '__main__':
    app.run()
