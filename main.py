from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,DecimalField, DateField
from wtforms.validators import DataRequired, NumberRange, Email, Length
from flask_sqlalchemy import SQLAlchemy
#import mysql.connector
from datetime import datetime

#creating flask instance
app = Flask(__name__)

#add database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/Employees'

#secret Key
app.config['SECRET_KEY'] = 'lmao-ded'

#init db
db = SQLAlchemy(app)

#create Model
class Employees(db.Model):
    __tablename__='Employees'

    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Department = db.Column(db.String(50))
    Salary = db.Column(db.Numeric(10, 2))
    JoiningDate = db.Column(db.Date, nullable=True)

#Create a from Class
class EmployeeForm(FlaskForm):
    Name=StringField("what is your name", validators=[DataRequired(), Length(max=100)])
    Email=StringField("Enter Email ID", validators=[DataRequired(), Email(),Length(max=100)])
    Department=StringField("Enter Department", validators=[DataRequired(), Length(max=50)])
    Salary=DecimalField("Enter Salary", places=2, rounding=None, validators=[DataRequired(), NumberRange(min=0)])
    JoiningDate=DateField("Enter Joining Date", validators=[DataRequired()])
    submit=SubmitField("Submit")

#Filters
# safe 
# capitalize
# lower
# upper
# title
# trim
# striptags

#Route for deleting entries
@app.route('/delete/<int:EmployeeID>')
def delete(EmployeeID):
    user_to_delete=Employees.query.get_or_404(EmployeeID)
    Name = None
    Email = None
    Department = None
    Salary = None
    JoiningDate = None
    form=EmployeeForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")

        our_users = Employees.query.order_by(Employees.EmployeeID).all()

        return render_template('form.html',
                            form=form,
                            Name=Name,
                            Email=Email,
                            Department=Department,
                            Salary=Salary,
                            JoiningDate=JoiningDate,
                            our_users=our_users)

    except:
        flash("There was an error Deleting")
        return render_template('form.html',
                           form=form,
                           Name=Name,
                           Email=Email,
                           Department=Department,
                           Salary=Salary,
                           JoiningDate=JoiningDate,
                           our_users=our_users)


#route for updating entries
@app.route('/update/<int:EmployeeID>', methods=['GET', 'POST'])
def update(EmployeeID):
    form = EmployeeForm()
    name_to_update = Employees.query.get_or_404(EmployeeID)
    if request.method == "POST":
        name_to_update.Department = request.form['Department']
        name_to_update.Salary = request.form['Salary']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   EmployeeID=EmployeeID)
        except:
            flash("Error Occured")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   EmployeeID=EmployeeID)
    else:
        return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   EmployeeID=EmployeeID)

#home page
@app.route("/")
# def index():
#     return "<h1>Hello</h1>"
def index():
    employees = Employees.query.order_by(Employees.EmployeeID).all()
    return render_template('index.html', employees=employees)

#test
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

#error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Route for data entry form
@app.route('/form', methods=['GET', 'POST'])
def form():
    Name = None
    Email = None
    Department = None
    Salary = None
    JoiningDate = None
    form=EmployeeForm()
    if form.validate_on_submit():
        user = Employees.query.filter_by(Email=form.Email.data).first()
        if user is None:
            user = Employees(Name=form.Name.data, 
                             Email=form.Email.data,
                             Department=form.Department.data,
                             Salary=form.Salary.data,
                             JoiningDate=form.JoiningDate.data
                             )
            db.session.add(user)
            db.session.commit()
        Name = form.Name.data
        Email = form.Email.data
        Department = form.Department.data
        Salary = form.Salary.data
        JoiningDate = form.JoiningDate.data
        form.Name.data = ''
        form.Email.data = ''
        form.Department.data = ''
        form.Salary.data = ''
        form.JoiningDate.data = ''

        flash("User Added Successfully!")

    our_users = Employees.query.order_by(Employees.EmployeeID).all()

    return render_template('form.html',
                           form=form,
                           Name=Name,
                           Email=Email,
                           Department=Department,
                           Salary=Salary,
                           JoiningDate=JoiningDate,
                           our_users=our_users)

#test logic 
# def form():
#     form=EmployeeForm()
#     field_names = ['Name', 'Email', 'Department', 'Salary', 'JoiningDate']
#     form_data = dict.fromkeys(field_names, None)
#     #validate Form
#     if form.validate_on_submit():
#         for field in field_names:
#             form_data[field] = getattr(form, field).data
#             getattr(form, field).data = ''
#     return render_template('form.html',form=form,
#                            **form_data)