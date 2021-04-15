from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, IntegerField, RadioField
from wtforms.validators import InputRequired


class AddSnackForm(FlaskForm):

    name = StringField("Snack Name", validators=[InputRequired(message="Snack can't be blank")])
    price = FloatField("Price in USD", validators=[InputRequired(message="Please use proper price format")])
    is_healthy = BooleanField("This is a healthy snack")
    quantity = IntegerField("How many")

    #category = RadioField("Category", choices=[('ic','Ice Cream'), ('chips', 'Potato Chips'), ('candy', 'Candy/Sweets')])
    category = SelectField("Category", choices=[('ic','Ice Cream'), ('chips', 'Potato Chips'), ('candy', 'Candy/Sweets')])

class EmployeeForm(FlaskForm):

   
    name = StringField("Employee Name", validators=[InputRequired(message="name cannot be blank")])
    state = StringField("State",  validators=[InputRequired()])
    dept_code = SelectField("Department Code")
    