from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, RadioField, DateTimeField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('An mich Erinnern')
    submit = SubmitField('Anmelden')

class ChildForm(FlaskForm):
    first_name = StringField('Vorname', validators=[DataRequired()])
    last_name = StringField('Nachname', validators=[DataRequired()])
    age = IntegerField('Alter', validators=[DataRequired()])
    group = SelectField('Gruppe', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], validators=[DataRequired()])
    # sleep_start = StringField('Schlafbeginn')
    # sleep_end = StringField('Schlafende')
    # food = SelectField('Essen', choices=[('Apfel', 'Apfel'), ('Birne', 'Birne')])
    # activities = StringField('Aktivitäten')
    submit = SubmitField('Speichern')

class EditChildForm(FlaskForm):
    first_name = StringField('Vorname', validators=[DataRequired()])
    last_name = StringField('Nachname', validators=[DataRequired()])
    age = IntegerField('Alter', validators=[DataRequired()])
    group = SelectField('Gruppe', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], validators=[DataRequired()])
    # sleep_start = DateTimeField('Schlafbeginn')
    # sleep_end = DateTimeField('Schlafende')
    # food = SelectField('Essen', choices=[('Apfel', 'Apfel'), ('Birne', 'Birne')])
    # activities = StringField('Aktivitäten')
    submit = SubmitField('Speichern')
    # change_type = RadioField('Windeltyp', choices=[('gross', 'Windel gewechselt groß'), ('klein', 'Windel gewechselt klein')])
    # submit_change = SubmitField('Windelwechsel bestätigen')

    def __init__(self, *args, **kwargs):
        super(EditChildForm, self).__init__(*args, **kwargs)

class DeleteChildForm(FlaskForm):
    confirmation = BooleanField('Bist du sicher?', validators=[DataRequired()])
    submit = SubmitField('Löschen')


    def __init__(self, *args, **kwargs):
        super(DeleteChildForm, self).__init__(*args, **kwargs)

    def validate_confirmation(self, field):
        if not field.data:
            raise ValidationError('Du musst bestätigen, dass du das Kind wirklich löschen möchtest.')
        
class AddActivityForm(FlaskForm):
    # Schlaf
    sleep_start_button = SubmitField('Schlaf Start')
    sleep_end_button = SubmitField('Schlaf Ende')
    
    # Essen
    food_choices = RadioField('Essen', choices=[('Apfel', 'Apfel'), ('Birne', 'Birne'), ('Andere', 'Andere')])
    other_food = StringField('Anderes Essen')  # Dieses Feld erscheint, wenn "Andere" ausgewählt ist
    
    # Windeln
    change_type = RadioField('Windelwechsel', choices=[('gross', 'Windel Gross'), ('klein', 'Windel Klein')])

    submit = SubmitField('Erfassen')

class PostForm(FlaskForm):
    # post = TextAreaField('Bitte melden Sie sich an', validators=[DataRequired()])
    login = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort Wiederholen', validators=[DataRequired(), EqualTo('password')])
    group = SelectField('Gruppenleiter', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], validators=[DataRequired()])
    submit = SubmitField('Registrieren')

class EditProfileForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password_active = PasswordField('Aktuelles Passwort', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort Wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Speichern')
    group = SelectField('Gruppe', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], validators=[DataRequired()])

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Bitte nutze einen anderen Benutzername.')
            
class AssignGroupForm(FlaskForm):
    new_group = SelectField('Gruppe', choices=[('A', 'A'), ('B', 'B'), ('C', 'C')])
    user_id = HiddenField()  # To keep track of which user we're updating
    submit = SubmitField('Gruppe zuweisen')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')