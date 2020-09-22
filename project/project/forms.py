from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User

class RegisterationForm(FlaskForm):
    # username = StringField('نام کاربری', 
    #                         validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "نام کاربری"})
    email = StringField('ایمیل',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "ایمیل"})
    password = PasswordField('رمز عبور', validators=[DataRequired()], render_kw={"placeholder": "رمز عبور"})
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "تکرار رمز عبور"})
    submit = SubmitField('ثبت نام')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('این ایمیل قبلا وارد شده است')

class LoginForm(FlaskForm):
    email = StringField('ایمیل',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "ایمیل"})
    password = PasswordField('رمز عبور', validators=[DataRequired()], render_kw={"placeholder": "رمز عبور"})
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField('ورود')
