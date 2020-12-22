from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask import request

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class IpAddForm(FlaskForm):
    ip = StringField('ip', validators=[DataRequired()])
    hostname = StringField('hostname', validators=[DataRequired()])	
    device_type = StringField('设备类型', validators=[DataRequired()])	
    user = StringField('使用者', validators=[DataRequired()])	
    project = StringField('应用', validators=[DataRequired()])	
    submit = SubmitField('确认')


class SearchForm(FlaskForm):
    q = StringField('全文搜索', validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

class UserAddForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('role', choices=[('1', 'admin'), ('2', 'general user')])
    submit = SubmitField('Rigister')