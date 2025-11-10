from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class AlbumForm(FlaskForm):
    title = StringField('Назва альбому', validators=[DataRequired(), Length(min=2, max=150)])
    release_year = IntegerField('Рік випуску')
    description = TextAreaField('Опис')
    submit = SubmitField('Зберегти')