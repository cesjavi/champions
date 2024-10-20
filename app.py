import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyectos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Carpeta para guardar imágenes subidas
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Inicializar la base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializar Flask-Migrate
# Modelo de Proyectos
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)  # Descripción de la tarea
    estado = db.Column(db.String(50), nullable=False, default="Pendiente")  # Estado de la tarea
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id'), nullable=False)  # Relación con Proyecto

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # Nombre del proyecto
    problema = db.Column(db.Text, nullable=False)  # Descripción del problema
    roadmap = db.Column(db.String(200))  # Enlace o referencia a un listado de tareas
    imagen = db.Column(db.String(200))
    pasos = db.relationship('Step', backref='proyecto', lazy=True, cascade="all, delete-orphan")

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)  # Descripción del paso o tarea
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyecto.id'), nullable=False)  # Relación con Proyecto
    orden = db.Column(db.Integer, nullable=False)  # Orden del paso en el roadmap

@app.route('/proyectos/editar/<int:id>', methods=['GET', 'POST'])
def editar_proyecto(id):
    proyecto = Proyecto.query.get_or_404(id)

    if request.method == 'POST':
        proyecto.nombre = request.form['nombre']
        proyecto.problema = request.form['problema']
        
        # Si se carga una nueva imagen, se guarda
        imagen = request.files['imagen']
        if imagen:
            filename = secure_filename(imagen.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(filepath)
            proyecto.imagen = filepath
        
        try:
            db.session.commit()  # Guardar cambios en la base de datos
            return redirect('/proyectos')
        except:
            return 'Hubo un problema al actualizar el proyecto.'
    
    return render_template('editar_proyecto.html', proyecto=proyecto)
# Modelo de Usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

def serialize_proyecto(proyecto):
    return {
        'nombre': proyecto.nombre,
        'problema': proyecto.problema,
        'imagen': proyecto.imagen
    }


# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Rutas para Proyectos
@app.route('/proyectos')
def proyectos():
    proyectos = Proyecto.query.all()
    return render_template('proyectos.html', proyectos=proyectos)

@app.route('/proyectos/agregar', methods=['POST', 'GET'])
def agregar_proyecto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']

        # Guardar la imagen si se subió
        if imagen:
            filename = secure_filename(imagen.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(filepath)  # Guardar la imagen en la carpeta de uploads
            ruta_imagen = filepath  # Guardar la ruta de la imagen en la base de datos
        else:
            ruta_imagen = None

        nuevo_proyecto = Proyecto(nombre=nombre, descripcion=descripcion, imagen=ruta_imagen)

        try:
            db.session.add(nuevo_proyecto)
            db.session.commit()
            return redirect('/proyectos')
        except:
            return 'Hubo un problema al agregar el proyecto'
    else:
        return render_template('agregar_proyecto.html')

@app.route('/quest-zone')
def quest_zone():
    proyectos = Proyecto.query.all()  # Obtener todos los proyectos de la base de datos
    proyectos_serializados = [serialize_proyecto(proyecto) for proyecto in proyectos]
    return render_template('quest_zone.html', proyectos=proyectos_serializados)


# Ruta para ver la página de Usuarios
@app.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

# Ruta para ver la página de Ayuda
@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

if __name__ == '__main__':
    app.run(debug=True)
