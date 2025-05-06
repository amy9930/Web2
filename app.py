from flask import Flask, render_template, request
from config import Config
from models import db, usuario, tarea

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
    tareas = ["Lavar la ropa", "Limpiar la casa", "Hacer la compra", "Estudiar para el examen", "Hacer ejercicio", "Leer un libro"]
    return render_template('tasks.html', tareas=tareas)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        return f"<p>{nombre}, {correo}, {contrasena}<p>"
    return render_template('signup.html')

@app.route('/task/create')
def create_task():
    return render_template('create_task.html')

@app.route('/task')
def task():
    return render_template('task.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)