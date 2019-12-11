import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ExptForm, UpdateExptForm,AddProductForm, AddEquipmentForm, AddReagentForm
from flaskDemo.models import User, Post, Employee, Project, Experiment, Reagent,Equipment,Product, Uses_Equipment, Uses_Reagent
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    results = Experiment.query.all()
    return render_template('experiment_home.html', outString = results)

    results3 = Employee.query.join(Works_On,Employee.ssn == Works_On.essn) \
               .add_columns(Employee.fname, Employee.lname, Works_On.essn, Works_On.pno, Works_On.hours) \
               .join(Project, Works_On.pno == Project.pnumber).add_columns(Project.pname, Project.pnumber)
    return render_template('assign_home.html', joined_m_n=results3)
    return render_template('dept_home.html', outString = results)
    posts = Post.query.all()
    return render_template('home.html', posts=posts)
    results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
               .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
               .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
    results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
              .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
    return render_template('join.html', title='Join', joined_1_n=results, joined_m_n=results2, joined_m_n3=results3)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/expt/<experiment_ID>")
@login_required
def expt(experiment_ID):
    expt = Experiment.query.get_or_404(experiment_ID)
    product = Product.query.join(Experiment, Experiment.experiment_ID == Product.experiment_ID).filter(Product.experiment_ID == experiment_ID)
    reagent = Uses_Reagent.query.join(Experiment, Experiment.experiment_ID == Uses_Reagent.experiment_ID).filter(Uses_Reagent.experiment_ID == experiment_ID)
    equipment = Uses_Equipment.query.join(Experiment, Experiment.experiment_ID == Uses_Equipment.experiment_ID).filter(Uses_Equipment.experiment_ID == experiment_ID)
    return render_template('experiment.html', title=expt.experiment_ID, expt=expt, now=datetime.utcnow(), product=product, reagent=reagent, equipment=equipment)


@app.route("/expt/new", methods=['GET', 'POST'])
@login_required
def new_expt():
    form = ExptForm()
    if form.validate_on_submit():
        print("helllo")
        expt = Experiment(experiment_ID = form.experiment_ID.data, project_ID =form.project_ID.data,employee_ID =form.employee_ID.data,
                          experiment_Objective=form.experiment_Objective.data, date = form.date.data, results = form.results.data)
        db.session.add(expt)
        db.session.commit()
        flash('You have added a new experiment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_expt.html', title='New Experiment',
                           form=form, legend='New Experiment')


@app.route("/expt/<experiment_ID>/update", methods=['GET', 'POST'])
@login_required
def update_experiment(experiment_ID):
    expt = Experiment.query.get_or_404(experiment_ID)
    currentExptObjective = expt.experiment_Objective
    currentExptResult = expt.results  
    currentExptDate = expt.date
    form = UpdateExptForm()
    if form.validate_on_submit():  
        if currentExptObjective !=form.experiment_Objective.data:  # notice we are are not passing the dnumber from the form
            expt.experiment_Objective=form.experiment_Objective.data
        if currentExptResult != form.results.data:
            expt.results = form.results.data
        if currentExptResult != form.date.data:
            expt.date = form.date.data
        db.session.commit()
        flash('Your experiment has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        form.experiment_Objective.data = expt.experiment_Objective
        form.results.data = expt.results
    return render_template('create_expt.html', title='Update Experiment',
                           form=form, legend='Update Experiment')


@app.route("/expt/<experiment_ID>/delete", methods=['POST'])
@login_required
def delete_experiment(experiment_ID):
    expt = Experiment.query.get_or_404(experiment_ID)
    db.session.delete(expt)
    db.session.commit()
    flash('The experiment has been deleted!', 'success')
    return redirect(url_for('home'))

# Deng gets here Dec 4, 11:30 pm

@app.route("/reagentList")
def reagentList():
    results = Reagent.query.all()
    return render_template('reagentList.html', outString = results)

@app.route("/equipmentList")
def equipmentList():
    results = Equipment.query.all()
    return render_template('equipmentList.html', outString = results)

@app.route("/experimentList")
def experimentList():
    results = Experiment.query.join(Employee,Employee.employee_ID == Experiment.employee_ID) \
    .add_columns(Employee.name,Employee.employee_ID,Experiment.experiment_ID)
    return render_template('experiment_list.html', outString = results)

@app.route("/addProduct/<experiment_ID>", methods=['GET', 'POST'])
@login_required
def addProduct(experiment_ID):
    form = AddProductForm()
    if form.validate_on_submit():
        prdt = Product(experiment_ID = experiment_ID, product_Name =form.product_Name.data, description =form.description.data,
                          location=form.location.data)
        db.session.add(prdt)
        db.session.commit()
        flash('You have added a new product!', 'success')
        return redirect(url_for('expt', experiment_ID=experiment_ID))
    elif request.method == 'GET':              
        form.experiment_ID.data = experiment_ID
    return render_template('add_prdt.html', title='Add Product',
                           form=form, legend='Add Product')

@app.route("/addEquipment/<experiment_ID>", methods=['GET', 'POST'])
@login_required
def addEquipment(experiment_ID):
    form = AddEquipmentForm()
    if form.validate_on_submit():
        uses_equip = Uses_Equipment(experiment_ID=experiment_ID, equipment_ID=form.equipment_ID.data, date=form.date.data)
        db.session.add(uses_equip)
        db.session.commit()
        flash('You have added a new equipment!', 'success')
        return redirect(url_for('expt', experiment_ID=experiment_ID))
    elif request.method == 'GET':              
        form.experiment_ID.data = experiment_ID
    return render_template('add_equip.html', title='Add Equipment',
                           form=form, legend='Add Equipment')

@app.route("/addReagent/<experiment_ID>", methods=['GET', 'POST'])
@login_required
def addReagent(experiment_ID):
    form = AddReagentForm()
    if form.validate_on_submit():
        uses_reag = Uses_Reagent(catalog_number=form.catalog_number.data, experiment_ID=experiment_ID, 
            quantity_used=form.quantity_used.data)
        db.session.add(uses_reag)
        db.session.commit()
        flash('You have added a new reagent!', 'success')
        return redirect(url_for('expt', experiment_ID=experiment_ID))
    elif request.method == 'GET':              
        form.experiment_ID.data = experiment_ID
    return render_template('add_reag.html', title='Add Reagent', 
                            form=form, legend='Add Reagent')

    