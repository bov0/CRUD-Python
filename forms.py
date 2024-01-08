from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp
from wtforms.fields import DateField
from modelos import Especie,Habitat


class AnimalForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Regexp('^[a-zA-Z\\s]+$', message='El nombre no puede contener números.')])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[DataRequired()], format='%Y-%m-%d')
    edad = StringField('Edad', validators=[DataRequired()])
    id_especie = SelectField('Especie')

    id_habitat = SelectField('Hábitat')

    def __init__(form, *args, **kwargs):
        super(AnimalForm, form).__init__(*args, **kwargs)
        form.id_especie.choices = [(str(especie.id_especie), especie.nombre_especie) for especie in Especie.query.all()]
        form.id_habitat.choices = [(str(habitat.id_habitat), habitat.nombre_habitat) for habitat in Habitat.query.all()]
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten archivos con las extensiones jpg, jpeg o png.')])
    submit = SubmitField('Añadir animal')
    
class EspecieForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Regexp('^[a-zA-Z\\s]+$', message='El nombre no puede contener números.')])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Añadir especie')

class HabitatForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Regexp('^[a-zA-Z\\s]+$', message='El nombre no puede contener números.')])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten archivos con las extensiones jpg, jpeg o png.')])
    submit = SubmitField('Añadir hábitat')