from flask import Flask, render_template, request, redirect , url_for, flash
import os

app = Flask(__name__)

from database import app, db, AnimalSchema
from modelos import Animal,Especie,Habitat

animal_schema = AnimalSchema()
animales_schema = AnimalSchema(many=True)

@app.route('/')
def index():
    todosAnimales = Animal.query.all()
    todasEspecies = Especie.query.all()
    todosHabitats = Habitat.query.all()
    return render_template('index.html', animales=todosAnimales, especies=todasEspecies, habitats=todosHabitats)

@app.route('/insertar', methods=['POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        id_especie = request.form['id_especie']
        id_habitat = request.form['id_habitat']

        if 'imagen' in request.files:
            imagen = request.files['imagen']
            
            extensiones = {'png', 'jpg', 'jpeg', 'gif'}
            if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() in extensiones:
                # Convierte el nombre del archivo a bytes
                filename_bytes = imagen.filename.encode('utf-8')

                # Guarda la imagen en el sistema de archivos
                filename = imagen.filename
                imagen.save(os.path.join("./img", filename))

                animal = Animal(nombre, fecha_nacimiento, edad, filename_bytes, id_especie, id_habitat)
                db.session.add(animal)
                db.session.commit()

                flash('Animal añadido correctamente')
                return redirect(url_for('index'))
            else:
                flash('Extensión de archivo no permitida')
                return redirect(url_for('index'))
        else:
            flash('Error al cargar la imagen del animal')
            return redirect(url_for('index'))


@app.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        animal = Animal.query.get(request.form.get('id'))
        animal.nombre_animal = request.form['nombre']
        animal.fecha_nacimiento = request.form['fecha_nacimiento']
        animal.edad = request.form['edad']
        # Verificamos si se proporciona una nueva imagen
        nueva_imagen = request.files.get('imagen')
        if nueva_imagen:
            animal.imagen = nueva_imagen.read()

        animal.id_especie = request.form['id_especie']
        animal.id_habitat = request.form['id_habitat']

        db.session.commit()
        flash('Animal actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/eliminar/<id>', methods=['GET', 'POST'])
def eliminar(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    flash('Animal eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
