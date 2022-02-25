from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class NewPasswordForm(FlaskForm):
    website = StringField("Website", validators=[DataRequired()])
    user = StringField("User", validators=[DataRequired()])
    passphrase = StringField("Passphrase", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditPasswordForm(FlaskForm):
    website = StringField("Website", validators=[DataRequired()])
    user = StringField("User", validators=[DataRequired()])
    passphrase = PasswordField("Passphrase", validators=[DataRequired()])
    submit = SubmitField("Update")


class DeletePasswordForm(FlaskForm):
    submit = SubmitField("Delete")


class SearchForm(FlaskForm):
    search = StringField("Search")
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    challenge = PasswordField("Challenge")
    submit = SubmitField("Submit")
