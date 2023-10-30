
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,RadioField,DateField, SelectField, SelectMultipleField, FileField
from wtforms.validators import Email,DataRequired,EqualTo,Length




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

class post(FlaskForm):
    username = StringField("username",validators=[DataRequired(message="The username is a must")])
    user_email = StringField("email",validators=[DataRequired(message="The email is a must")])
    bio = StringField("bio",validators=[DataRequired(message="The bio is a must")])
    submit =SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(message="The Username is a must")])
    password = PasswordField(validators=[DataRequired(message="Enter Password")])
    btnsubmit = SubmitField("Register!")

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Subtitle', validators=[DataRequired()])
    subcontent = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')
    categories = SelectField('Categories', choices=[
    ('Programming', 'Programming'),
    ('Hardware', 'Hardware'),
    ('Software', 'Software'),
    ('AI & Machine Learning', 'AI & Machine Learning'),
    ('Web Development', 'Web Development'),
    ('Mobile Development', 'Mobile Development'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Gaming', 'Gaming'),
    ('IoT (Internet of Things)', 'IoT (Internet of Things)'),
    ('Tech News', 'Tech News'),
    ('Reviews', 'Reviews'),
    ('Tutorials', 'Tutorials'),
    ('Blogging and Opinion', 'Blogging and Opinion'),
    ('Science and Technology', 'Science and Technology'),
    ('AI Ethics and Society', 'AI Ethics and Society'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Cloud Computing', 'Cloud Computing'),
    ('E-commerce', 'E-commerce'),
    ('Startup and Entrepreneurship', 'Startup and Entrepreneurship'),
    ('Networking', 'Networking')
])

    tags = StringField('Tag') 


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    message = TextAreaField('Message', validators=[DataRequired()])

