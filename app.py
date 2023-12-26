from flask import Flask, render_template, request, redirect , url_for, flash, send_file
from io import BytesIO
import os
from werkzeug.utils import secure_filename
from forms import AnimalForm, EspecieForm, HabitatForm

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

@app.route('/habitats')
def habitats():
    todosAnimales = Animal.query.all()
    todasEspecies = Especie.query.all()
    todosHabitats = Habitat.query.all()
    return render_template('habitats.html', animales=todosAnimales, especies=todasEspecies, habitats=todosHabitats)

@app.route('/especies')
def especies():
    todosAnimales = Animal.query.all()
    todasEspecies = Especie.query.all()
    todosHabitats = Habitat.query.all()
    return render_template('especies.html', animales=todosAnimales, especies=todasEspecies, habitats=todosHabitats)

@app.route('/insertarAnimal', methods=['POST'])
def insertarAnimal():
    form = AnimalForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        fecha_nacimiento = form.fecha_nacimiento.data
        edad = form.edad.data
        id_especie = form.id_especie.data
        id_habitat = form.id_habitat.data

        imagen = form.imagen.data
        if imagen:
            filename = imagen.filename
            extensiones = {'png', 'jpg', 'jpeg'}
            if '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones:
                datos_imagen = imagen.read()
                ruta_imagen = os.path.join("./static/img", filename)
                imagen.save(ruta_imagen)

                animal = Animal(nombre_animal=nombre, fecha_nacimiento=fecha_nacimiento, edad=edad, id_especie=id_especie, id_habitat=id_habitat, nombre_Imagen=ruta_imagen, imagen=datos_imagen)
                db.session.add(animal)
                db.session.commit()

                flash('Animal añadido correctamente')
                return redirect(url_for('index'))
            else:
                flash('Extensión de archivo no permitida')
        else:
            flash('Error al cargar la imagen del animal')
    else:
        for field, errors in form.errors.items():
            # Ignora el error CSRF Token
            if field != 'csrf_token':
                for error in errors:
                    flash(f'Error en el campo {getattr(form, field).label.text}: {error}')
    return redirect(url_for('index'))

            
@app.route('/insertarEspecie', methods=['POST'])
def insertarEspecie():
    form = EspecieForm()

    if form.validate_on_submit():
        nombre = form.nombre.data
        descripcion = form.descripcion.data

        nueva_especie = Especie(nombre_especie=nombre, descripcion=descripcion)
        db.session.add(nueva_especie)
        db.session.commit()

        flash('Especie añadida correctamente', 'success')
        return redirect(url_for('index'))
    else:
        for field, errors in form.errors.items():
            # Ignora el error CSRF Token
            if field != 'csrf_token':
                for error in errors:
                    flash(f'Error en el campo {getattr(form, field).label.text}: {error}')

    return redirect(url_for('index'))

@app.route('/insertarHabitat', methods=['POST'])
def insertarHabitat():
    form = HabitatForm()

    if form.validate_on_submit():
        nombre = form.nombre.data

        nuevo_habitat = Habitat(nombre_habitat=nombre)

        # Manejar la imagen si se proporciona
        if form.imagen.data:
            imagen = form.imagen.data
            datos_imagen = imagen.read()
            filename = secure_filename(imagen.filename)
            ruta_imagen = os.path.join("./static/img", filename)
            imagen.save(ruta_imagen)
            nuevo_habitat.nombre_imagen = ruta_imagen
            nuevo_habitat.imagen_habitat = datos_imagen

        db.session.add(nuevo_habitat)
        db.session.commit()

        flash('Habitat añadido correctamente', 'success')
    else:
        for field, errors in form.errors.items():
            # Ignora el error CSRF Token
            if field != 'csrf_token':
                for error in errors:
                    flash(f'Error en el campo {getattr(form, field).label.text}: {error}')

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
    especie = animal.especie
    habitat = animal.habitat
    return render_template('mostrarAnimal.html', animal=animal, especie=especie, habitat=habitat)

@app.route('/verImagen/<id>')
def imagen_animal(id):
    animal = Animal.query.get(id)

    if animal and animal.imagen:
        try:
            # Convierte el campo BLOB a un objeto BytesIO
            imagen_bytes = BytesIO(animal.imagen)

            # Envia la imagen al navegador con el tipo MIME adecuado
            return send_file(imagen_bytes, mimetype='image/jpeg')
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al convertir o enviar la imagen
            print(f"Error al cargar la imagen: {e}")
            return send_file('./static/img/Cool wallpaper.jpg', mimetype='image/jpeg')
    else:
        # Si no hay imagen o el animal no existe, enviar una imagen de reemplazo o error 404
        return send_file('./static/img/Cool wallpaper.jpg', mimetype='image/jpeg')


@app.route('/verHabitat/<id>')
def imagen_habitat(id):
    habitat = Habitat.query.get(id)
    
    if habitat and habitat.nombre_imagen:  
        imagen_bytes = BytesIO(habitat.imagen_habitat)
        
        # Obtener la ruta absoluta del archivo
        return send_file(imagen_bytes, mimetype='image/jpeg')
        
    
    # Si no hay imagen o el hábitat no existe, enviar una imagen de reemplazo o un error 404
    return send_file('./static/img/ZPFFQI~1.PNG', mimetype='image/jpeg')

@app.route('/animalesHabitat/<int:habitat_id>')
def animalesHabitat(habitat_id):
    # Aquí obtienes los animales que pertenecen al hábitat con el ID proporcionado
    habitat = Habitat.query.get(habitat_id)
    animales_en_habitat = habitat.animales

    return render_template('animalesHabitat.html', habitat=habitat, animales=animales_en_habitat)


@app.route('/eliminar/<id>', methods=['GET', 'POST'])
def eliminar(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    flash('Animal eliminado correctamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
