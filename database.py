from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv, find_dotenv
import os

# Lee la información existente en un archivo denominado .env
# Este es un archivo oculto en un servidor de producciómn y alberga
# las etiquetas y sus valores para la cadena de conexión a MongoDB


load_dotenv(find_dotenv())
usuario = os.environ.get("MYSQLDB_USUARIO")
password = os.environ.get("MYSQLDB_PASSWORD")
host = os.environ.get("MYSQLDB_HOST")
bd = os.environ.get("MYSQLDB_BD")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{usuario}:{password}@{host}/{bd}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hardsecretkey'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class EspecieSchema(ma.Schema):
    class Meta:
        fields = ('id_especie', 'nombre_especie', 'descripcion')

class HabitatSchema(ma.Schema):
    class Meta:
        fields = ('id_habitat', 'nombre_habitat' ,'nombre_imagen' ,'imagen_habitat')

class AnimalSchema(ma.Schema):
    class Meta:
        fields = ('id_animal', 'nombre_animal', 'fecha_nacimiento', 'edad', 'id_especie', 'id_habitat','nombre_Imagen' ,'imagen')
