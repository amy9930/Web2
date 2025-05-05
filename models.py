from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.colum(db.interger, primary_key=True)
    nombre = db.column(db.String(200), nullable=False)
    correo = db.column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.column(db.String (256), nulable=False)

    tareas = db.relationship('tarea', backref='usuario', lazy=True)
    def colocar_cantraseña(self, contraseña):
        self.contrasena_hash = generate_password_hash(contraseña)
    
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contrasena_hash, contraseña)

class tarea(db.Model):
    __tablename__ = 'tareas'

    id = db.colum(db.interger, primary_key=True)
    titulo = db.colum(db.String(200), nullable=False)
    descripcion = db column(db.txt, nullable=True)
    fecha_creacion = db.column(db.datetime)
    prioridad = db.column(db.string(50), nullable=False)
    usuario_id = db.integer, db. foreign_key
