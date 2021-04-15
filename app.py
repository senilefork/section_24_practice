from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import Employee, Department, db, connect_db
from forms import AddSnackForm, EmployeeForm
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///employees_db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "abc123"

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route("/phones")
def phone_list():
    """Get list of users & dept phones.

    This version will be a 'n+1 query' --- it will query once for all
    users, and then for each department.

    There's a way to tell SQLAlchemy to load all the data in a single query,
    but don't worry about this for now.
    """

    emps = Employee.query.all()
    return render_template("phones.html", emps=emps)

@app.route('/')
def home_page():
    return render_template("home.html")

@app.route('/snacks/new', methods=["GET","POST"])
def add_snack():
    #print(request.form)
    form = AddSnackForm()

    if form.validate_on_submit():
    #is this a post request and is the toekn valid?
        data = request.form
        name = form.name.data
        price = form.price.data
        flash(f"created new snack name is {name}, price is ${price}, {data}")
        return redirect('/')
    else:
        return render_template("add_snack_form.html", form=form)

@app.route('/employees/new', methods=["GET", "POST"])
def add_employee():
    form = EmployeeForm()
    depts = db.session.query(Department.dept_code, Department.dept_name)
    #pdb.set_trace()
    #depts = [('mktg','Marketing')]
    form.dept_code.choices = depts
    #raise 
   
    if form.validate_on_submit():
        name = form.name.data
        state = form.state.data
        dept_code = form.dept_code.data

        emp = Employee(name=name, state=state, dept_code=dept_code)
        db.session.add(emp)
        db.session.commit()
        return redirect('/phones')
    else:
        return render_template('add_employee.html', form=form)

@app.route('/employees/<int:id>/edit', methods=["GET", "POST"])
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=emp)
    depts = [('mktg','Marketing')]
    form.dept_code.choices = depts

    if form.validate_on_submit():
        emp.name = form.name.data
        emp.state = form.state.data
        emp.dept_code = form.dept_code.data
        db.session.commit()
        return redirect('/phones')
    else:
        return render_template("edit_employee_form.html", form=form)

