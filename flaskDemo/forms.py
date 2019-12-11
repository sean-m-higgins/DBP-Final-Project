from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Project, Employee, Product, Uses_Reagent, Uses_Equipment, Reagent, Equipment
from wtforms.fields.html5 import DateField

# for that way, we would have imported db from flaskDemo, see above
projIDs=Project.query.with_entities(Project.project_ID).distinct()
projChoices = [(row[0],row[0]) for row in projIDs]

emplyIDs=Employee.query.with_entities(Employee.employee_ID).distinct()
emplChoices = [(row[0],row[0]) for row in emplyIDs]

cat_num=Reagent.query.with_entities(Reagent.catalog_number).distinct()
cat_numChoices = [(row[0],row[0]) for row in cat_num]

equip_ID=Equipment.query.with_entities(Equipment.equipment_ID).distinct()
equipChoices = [(row[0],row[0]) for row in equip_ID]


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

class ExptForm (FlaskForm):
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

class UpdateExptForm (FlaskForm):
    experiment_Objective = StringField("Objective", validators = [DataRequired(),Length (max=100)])
    date = DateField("Experiment date:", format='%Y-%m-%d')
    results = TextAreaField("Results")
    submit = SubmitField('Update this experiment')

class AddProductForm(FlaskForm):
    experiment_ID =HiddenField("")
    product_Name= StringField("Product Name:", validators = [DataRequired(),Length (max=50)])
    description= TextAreaField("Product Description:", validators=[DataRequired()])
    location= TextAreaField("Product location:", validators=[DataRequired()])
    submit = SubmitField('Add this product')
    def validate_product(self, product_Name):
        prod = Product.query.filter_by(experiment_ID=self.experiment_ID.data, product_Name=product_Name.data).first()
        if prod:
            raise ValidationError('That product name is already used. Please choose a different product name.')

class AddEquipmentForm(FlaskForm):
    experiment_ID =HiddenField("")
    equipment_ID= SelectField("Equipment ID:", choices = equipChoices)
    date = DateField("Experiment date:", format='%Y-%m-%d')
    submit = SubmitField('Add this equipment')
    def validate_product(self, equipment_ID):
        equip = Uses_Equipment.query.filter_by(experiment_ID=self.experiment_ID.data, equipment_ID=equipment_ID.data).first()
        if equip:
            raise ValidationError('That equipment ID is already used. Please choose a different equipment ID.')

class AddReagentForm(FlaskForm): 
    experiment_ID =HiddenField("")  
    catalog_number= SelectField("Catalogue Number", choices = cat_numChoices)
    quantity_used= IntegerField("Quantity Used", validators=[DataRequired()])
    submit = SubmitField('Add this reagent')
    def validate_product(self, catalogue_number):
        cat_num = Uses_Reagent.query.filter_by(experiment_ID=self.experiment_ID.data, catalogue_number=catalogue_number.data).first()
        if cat_num:
            raise ValidationError('That product name is already used. Please choose a different product name.')
