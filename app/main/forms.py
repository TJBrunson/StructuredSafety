from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FormField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Document

class AddDocument(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    tag = SelectField('tag', choices=[('Policies', 'Policies'), 
        ('Safety Data Sheets', 'Safety Data Sheets'), 
        ('Forms', 'Forms'),
        ('Misc', 'Miscellaneous')], validators=[DataRequired()])
    document = FileField('document', validators=[FileRequired()])
    submit = SubmitField('Add Document')