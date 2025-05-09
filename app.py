from flask import Flask, render_template, request, url_for, redirect, session
from config import Config
from models import db, usuario, tarea
from datetime import datetime
app = Flask(__name__)
#configuraciòn de la aplicaciòn flask (donde se indica la base de datos)
app.config.from_object(Config)
#instalar la base de datos
db.init_app(app)
#crear base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tasks')
def list_tasks():
    tareas = tarea.query.filter_by(usuario_id=session["usuario_id"]).all()
    return render_template('tasks.html', tareas=tareas)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        Usuario = usuario.query.filter_by(correo=correo).first()
        if Usuario and Usuario.verificar_contrasena(contrasena):
            session["usuario_id"] = Usuario.id
            session["usuario_nombre"] = Usuario.nombre
            return redirect(url_for('list_tasks'))
        else:
            return "Correo o contraseña incorrectos."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        if usuario.query.filter_by(correo=correo).first():
            return "El correo esta registrado."
        else: 
            nuevo_usuario = usuario(nombre=nombre, correo=correo)
            nuevo_usuario.colocar_contrasena(contrasena)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))  
    return render_template('signup.html')

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_vencimiento = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        prioridad = request.form['prioridad']
        try:
            nueva_tarea = tarea(titulo=titulo, descripcion=descripcion, fecha_vencimiento=fecha_vencimiento, prioridad=prioridad, usuario_id=session['usuario_id'])
            db.session.add(nueva_tarea)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            return f"Error al crear la tarea: {e}"
    return render_template('create_task.html')


@app.route('/task')
def task():
    return render_template('task.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)