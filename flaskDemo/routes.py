import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, ExptForm, UpdateExptForm
from flaskDemo.models import User, Post, Employee, Project, Experiment
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


@app.route("/expt/new", methods=['GET', 'POST'])
@login_required
def new_expt():
    form = ExptForm()
    if form.validate_on_submit():
        expt = Experiment(experiment_ID = form.experiment_ID.data, project_ID =form.project_ID.data,employee_ID =form.employee_ID.data,
                          experiment_Objective=form.experiment_Objective.data, date = form.date.data, results = form.results.data)
        db.session.add(expt)
        db.session.commit()
        flash('You have added a new experiment!', 'success')
        return redirect(url_for('home'))
    return render_template('create_expt.html', title='New Experiment',
                           form=form, legend='New Experiment')


@app.route("/expt/<experiment_ID>")
@login_required
def expt(experiment_ID):
    expt = Experiment.query.get_or_404(experiment_ID)
    return render_template('experiment.html', title=expt.experiment_ID, expt=expt, now=datetime.utcnow())


@app.route("/expt/<experiment_ID>/update", methods=['GET', 'POST'])
@login_required
def update_experiment(experiment_ID):
    expt = Experiment.query.get_or_404(experiment_ID)
    currentExptObjective = expt.experiment_Objective
    currentExptResult = expt.results  

    form = UpdateExptForm()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
        if currentExptObjective !=form.experiment_Objective.data:
            expt.experiment_Objective=form.experiment_Objective.data
        if currentExptResult != form.results.data:
            expt.results = form.results.data
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

@app.route("/assign/<essn>/<pno>")
@login_required
def assign(essn, pno):
    assign = Works_On.query.get_or_404([essn,pno])
    return render_template('assign.html', title=str(assign.essn) + "_" + str(assign.pno), assign=assign, now=datetime.utcnow())

@app.route("/assign/new", methods=['GET', 'POST'])
@login_required
def new_assign():
    form = AssignForm()
    if form.validate_on_submit():
        return redirect(url_for('new_assign_pno', essn=form.essn.data, hours=form.hours.data))
    return render_template('create_assign.html', title='New ESSN Assignment',
                           form=form, legend='New ESSN Assignment')

@app.route("/assign/<essn>/<hours>/newPno", methods=['GET', 'POST'])
@login_required
def new_assign_pno(essn, hours):
    form = AssignFormPno()
    form.essn.data = essn
    if form.validate_on_submit():
        assign = Works_On(essn=essn, pno=form.pno.data, hours=hours)
        db.session.add(assign)
        db.session.commit()
        flash('You have added a new assignment!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':              
        form.essn.data = essn
    return render_template('create_assign.html', title='New Project Assignment',
                           form=form, legend='New Project Assignment')


@app.route("/assign/<essn>/<pno>/delete", methods=['POST'])
@login_required
def delete_assign(essn, pno):
    assign = Works_On.query.get_or_404([essn,pno])
    db.session.delete(assign)
    db.session.commit()
    flash('The assignment has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/assign/<essn>/<pno>/updateEssn", methods=['GET', 'POST'])
@login_required
def update_assign(essn, pno):
    assign = Works_On.query.get_or_404([essn,pno])
    currentEssn = assign.essn

    form = AssignUpdateEssnForm()
    form.pno.data = assign.pno
    if form.validate_on_submit():          
        if currentEssn != form.essn.data:
            assign.essn=form.essn.data
        db.session.commit()
        flash('Your Employee SSN has been saved!', 'success')
        return redirect(url_for('update_assign_pno', essn=form.essn.data, pno=pno))
    elif request.method == 'GET':              
        form.essn.data = assign.essn
        form.pno.data = assign.pno
    return render_template('create_assign.html', title='Update Employee SSN',
                           form=form, legend='Update Employee SSN')


@app.route("/assign/<essn>/<pno>/updatePno", methods=['GET', 'POST'])
@login_required
def update_assign_pno(essn, pno):
    assign = Works_On.query.get_or_404([essn,pno])
    currentProj = assign.pno

    form = AssignUpdatePnoForm()
    if form.validate_on_submit():
        if currentProj != form.pno.data:
            assign.pno= form.pno.data
        db.session.commit()
        flash('Your assignment has been updated!', 'success')
        return redirect(url_for('assign', essn=essn, pno=form.pno.data))
    elif request.method == 'GET':              
        form.pno.data = assign.pno
        form.essn.data = assign.essn
    return render_template('create_assign.html', title='Update Assignment',
                           form=form, legend='Update Assignment')

