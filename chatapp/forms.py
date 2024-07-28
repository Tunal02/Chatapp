from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError
from .model import User,Active_room
from .extensions import get_random_alphanumeric_string
class signupform(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=4,max=20)])
    password=PasswordField('password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',
                                   validators=[DataRequired(message='password Required'),EqualTo('password',message='passwords must match')])
    submit=SubmitField('Sign me up')
    def validate_username(self,username):
        user_obj=User.query.filter_by(username=username.data).first()
        if user_obj:
            raise  ValidationError('User name already exists')



class loginform(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=2,max=20)],)
    password=PasswordField('password',validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit=SubmitField('login please')


    def validate_login(self,username,password):
        Usr=User.query.filter_by(username=username.data).first()
        pswrd=User.query.filter_by(password=password).first()
        if not Usr:
            raise  ValidationError('Wrong password or Username !!')
        elif not pswrd:
            raise  ValidationError('Wrong password or Username !!')


class code(FlaskForm):
    code1 = get_random_alphanumeric_string()
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Create a Room')

    def validate_code(self, code):
        if code.data != self.code1:
            raise ValidationError('Invalid code. Please try again.')
        

class join(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Join a Room')

    def validate_code(self,code):
        room=Active_room.query.filter_by(room_id=self.code.data).first()
        if not room:
            raise ValidationError('Invalid code. Please try again.')

    
        


