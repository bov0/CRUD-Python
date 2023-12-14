from flask import Flask, render_template, request, redirect , url_for, flash, send_file
from io import BytesIO
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

@app.route('/insertarAnimal', methods=['POST'])
def insertarAnimal():
    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        id_especie = request.form['id_especie']
        id_habitat = request.form['id_habitat']

        if 'imagen' in request.files:
            imagen = request.files['imagen']
            
            extensiones = {'png', 'jpg', 'jpeg'}
            if '.' in imagen.filename and imagen.filename.rsplit('.', 1)[1].lower() in extensiones:
                filename_bytes = imagen.filename.encode('utf-8')

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
            
@app.route('/insertarEspecie', methods=['POST'])
def insertarEspecie():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        nueva_especie = Especie(nombre_especie=nombre, descripcion=descripcion)
        db.session.add(nueva_especie)
        db.session.commit()
        flash('Especie añadido correctamente')
        return redirect(url_for('index'))
    else:
                flash('Fallo al añadir especie')
                return redirect(url_for('index'))
    
@app.route('/insertarHabitat', methods=['POST'])
def insertarHabitat():
    if request.method == 'POST':
        nombre = request.form['nombre']


        nuevo_habitat = Habitat(nombre_habitat=nombre)
        db.session.add(nuevo_habitat)
        db.session.commit()
        flash('Habitat añadido correctamente')
        return redirect(url_for('index'))
    else:
                flash('Fallo al añadir Habitat')
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
    

@app.route('/mostrarAnimal/<id>')
def mostrarAnimal(id):
    animal = Animal.query.get(id)
    return render_template('mostrarAnimal.html', animal=animal)

@app.route('/verImagen/<id>')
def imagen_animal(id):
    animal = Animal.query.get(id)
    
    if animal and animal.imagen:
        # Convierte el campo BLOB a un objeto BytesIO
        imagen_bytes = BytesIO(animal.imagen)
        
        # Envia la imagen al navegador con el tipo MIME adecuado
        return send_file(imagen_bytes, mimetype='image/jpeg')
    
    # Si no hay imagen o el animal no existe, puedes enviar una imagen de reemplazo o un error 404
    return send_file('./img/ZPFFQI~1.PNG', mimetype='image/jpeg')

@app.route('/eliminar/<id>', methods=['GET', 'POST'])
def eliminar(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    flash('Animal eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
