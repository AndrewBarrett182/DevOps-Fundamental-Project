from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField, FloatField, IntegerField, SelectField
from wtforms.fields.simple import PasswordField

class Users(db.Model):
    username = db.Column(db.String(30), primary_key = True)
    password = db.Column(db.String(30), nullable = False)
    items = db.relationship('Inventory', backref = 'users')

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    stock = db.Column(db.Integer, default = 0)
    price = db.Column(db.Float, default = 0)
    for_sale = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'), nullable = False)

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    login = SubmitField('Login')
    register = SubmitField('Create a New Account')
    delete = SubmitField("Delete")
    back = SubmitField("Back")

class ItemsForm(FlaskForm):
    name = StringField("Item Name")
    add_item = SubmitField("Add New Item")
    update = SubmitField("Update Item Details")
    delete = SubmitField("Delete")
    order = SelectField('Sort by', choices = [("Oldest", "Oldest"), ("Newest", "Newest"), ("A-Z", "A-Z"), ("Z-A", "Z-A"), 
                                              ("Stock ↑", "Stock ↑"), ("Stock ↓", "Stock ↓"), ("Price ↑", "Price ↑"), 
                                              ("Price ↓", "Price ↓"), ("For Sale", "For Sale"), ("Not For Sale", "Not For Sale")])
    submit = SubmitField('Submit')
    back = SubmitField("Back")
    stock = IntegerField("Stock")
    price = FloatField("Price")
    for_sale = BooleanField("For Sale?")
    buy = SubmitField("Buy Item")
    # task = StringField('Task')
    # submit_task = SubmitField('Add Task')
    # complete = SubmitField('Complete Task')
    # incomplete = SubmitField('Incomplete Task')
    # delete = SubmitField('Delete Task')
    # update = SubmitField('Update Task')
    # order = SelectField('Sort by', choices = [("Oldest", "Oldest"), ("Newest", "Newest"), ("Completed", "Completed"), ("Not Completed", "Not Completed")])
    # submit_order = SubmitField('Submit')