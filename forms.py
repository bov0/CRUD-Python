from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp

class EspecieForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Regexp('^[a-zA-Z\\s]+$', message='El nombre no puede contener números.')])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Añadir especie')

class HabitatForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Regexp('^[a-zA-Z\\s]+$', message='El nombre no puede contener números.')])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten archivos con las extensiones jpg, jpeg o png.')])
    submit = SubmitField('Añadir hábitat')