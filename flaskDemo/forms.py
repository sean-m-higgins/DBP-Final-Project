from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Project, Employee, Product
from wtforms.fields.html5 import DateField

#ssns = Department.query.with_entities(Department.mgr_ssn).distinct()
#  or could have used ssns = db.session.query(Department.mgr_ssn).distinct()
# for that way, we would have imported db from flaskDemo, see above
projIDs=Project.query.with_entities(Project.project_ID).distinct()
projChoices = [(row[0],row[0]) for row in projIDs]

emplyIDs=Employee.query.with_entities(Employee.employee_ID).distinct()
emplChoices = [(row[0],row[0]) for row in emplyIDs]
#myChoices2 = [(row[0],row[0]) for row in ssns]  # change
#results=list()
#for row in ssns:
#    rowDict=row._asdict()
#    results.append(rowDict)
#myChoices = [(row['mgr_ssn'],row['mgr_ssn']) for row in results]
#regex1='^((((19|20)(([02468][048])|([13579][26]))-02-29))|((20[0-9][0-9])|(19[0-9][0-9]))-((((0[1-9])'
#regex2='|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))$'
#regex=regex1 + regex2


#essns = Works_On.query.with_entities(Works_On.essn).distinct()
#results_essn=list()
#for row in essns:
#    rowDict=row._asdict()
#    results_essn.append(rowDict)
#myEssnChoices = [(row['essn'],row['essn']) for row in results_essn]

#pnos = Works_On.query.with_entities(Works_On.pno).distinct()
#results_pno=list()
#for row in pnos:
#    rowDict=row._asdict()
#    results_pno.append(rowDict)
#myPnoChoices = [(row['pno'], row['pno']) for row in results_pno]
#myPno = [row['pno'] for row in results_pno]



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

    
#class DeptUpdateForm(FlaskForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#    dnumber = HiddenField("")

#    dname=StringField('Department Name:', validators=[DataRequired(),Length(max=15)])
#  Commented out using a text field, validated with a Regexp.  That also works, but a hassle to enter ssn.
#    mgr_ssn = StringField("Manager's SSN", validators=[DataRequired(),Regexp('^(?!000|666)[0-8][0-9]{2}(?!00)[0-9]{2}(?!0000)[0-9]{4}$', message="Please enter 9 digits for a social security.")])

#  One of many ways to use SelectField or QuerySelectField.  Lots of issues using those fields!!
#    mgr_ssn = SelectField("Manager's SSN", choices=myChoices)  # myChoices defined at top
    
# the regexp works, and even gives an error message
#    mgr_start=DateField("Manager's Start Date:  yyyy-mm-dd",validators=[Regexp(regex)])
#    mgr_start = DateField("Manager's Start Date")

#    mgr_start=DateField("Manager's Start Date", format='%Y-%m-%d')
#    mgr_start = DateField("Manager's start date:", format='%Y-%m-%d')  # This is using the html5 date picker (imported)
#    submit = SubmitField('Update this department')


# got rid of def validate_dnumber

#    def validate_dname(self, dname):    # apparently in the company DB, dname is specified as unique
#         dept = Department.query.filter_by(dname=dname.data).first()
#         if dept and (str(dept.dnumber) != str(self.dnumber.data)):
#             raise ValidationError('That department name is already being used. Please choose a different name.')

class ExptForm (FlaskForm):
    cur_experiment_ID = HiddenField("")
    experiment_ID =StringField("Experiment ID", validators = [DataRequired(),Length (max=4)])
    project_ID = SelectField("Project ID", choices=projChoices, validators=[DataRequired()])
    employee_ID = SelectField("Employee ID", choices=emplChoices, coerce=int, validators=[DataRequired()])
    experiment_Objective = StringField("Objective", validators = [DataRequired(),Length (max=100)])
    date = DateField("Experiment date:", format='%Y-%m-%d')
    results = TextAreaField("Results")
    submit = SubmitField('Create this experiment')
    def validate_exp_id(self, experiment_ID):
        exp = Experiment.query.filter_by(experiment_ID=experiment_ID.data).first()
        if exp:
            raise ValidationError('That experiment_ID is already used. Please choose a different experiment_ID.')





class UpdateExptForm (ExptForm):
    experiment_ID =HiddenField("")
    project_ID = HiddenField("")
    employee_ID = HiddenField("")
    experiment_Objective = StringField("Objective", validators = [DataRequired(),Length (max=100)])
    date = DateField("Experiment date:", format='%Y-%m-%d')
    results = StringField("Results")
    submit = SubmitField('Update this experiment')

class AddProductForm(FlaskForm):
    product_Name= StringField("product Name", validators = [DataRequired(),Length (max=50)])
    description= TextAreaField("Product Description", validators=[DataRequired()])
    location= TextAreaField("Product location", validators=[DataRequired()])
    submit = SubmitField('Add this product')
#class DeptForm(DeptUpdateForm):

#    dnumber=IntegerField('Department Number', validators=[DataRequired()])
#    submit = SubmitField('Add this department')

#    def validate_dnumber(self, dnumber):    #because dnumber is primary key and should be unique
#        dept = Department.query.filter_by(dnumber=dnumber.data).first()
#        if dept:
#            raise ValidationError('That department number is taken. Please choose a different one.')


#class AssignUpdateEssnForm(FlaskForm):
#    pno = HiddenField("")
#    essn = SelectField("Employee's SSN", choices=myEssnChoices)
#    submit = SubmitField('Update Employee SSN')

#    def validate_essn(self, essn):
        
#        assign = Works_On.query.filter_by(essn=essn.data, pno=self.pno.data).first()
#        if assign:
#            raise ValidationError('That employee is already assigned to the current project. Please choose a different project.')


#class AssignUpdatePnoForm(FlaskForm):
#    essn = HiddenField("")
#    pno = SelectField("Project Number", choices=myPnoChoices, coerce=int)
#    submit = SubmitField('Update this Assignment')

#    def validate_pno(self, pno):    
#        assign = Works_On.query.filter_by(essn=self.essn.data, pno=pno.data).first()
#        if assign:
#            raise ValidationError('That employee is already assigned to that project. Please choose a different project.')


#class AssignForm(FlaskForm):
#    hours = IntegerField("Hours", validators=[DataRequired()])
#    essn = SelectField("Employee's SSN", choices=myEssnChoices)
#    submit = SubmitField('Enter Employee SSN and Hours')

#    def validate_hours(self, hours):    
#        if hours.data < 0 or hours.data >= 100:
#            raise ValidationError('Hours must be a positive integer and less than 100. Please re-enter Hours.')


#class AssignFormPno(FlaskForm):
#    essn = HiddenField("")
#    pno = SelectField("Project Number", choices=myPnoChoices, coerce=int)
#    submit = SubmitField('Create this Assignment')

#    def validate_pno(self, pno):
#        print('he')
#        print(self.essn.data)
#        print('he')
#        assign = Works_On.query.filter_by(essn=self.essn.data, pno=pno.data).first()
#        if assign:
#            raise ValidationError('That employee is already assigned to that project. Please choose a different project.')



