from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1849@localhost/crud'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        
        return {"id": self.id, "nome": self.nome, "email": self.email}

#retornar usuarios cadastrados  
@app.route("/usuarios",methods=["GET"])
def ret_users():
    usuario_objetos = Usuario.query.all()
    usuarios_json = [usuarios.to_json() for usuarios in usuario_objetos]
    print(usuarios_json)

    return Response(json.dumps(usuarios_json))

#retorna um usuario especifico

#cadastrar usuario

#modificar usuario

#deletar usuario

app.run()