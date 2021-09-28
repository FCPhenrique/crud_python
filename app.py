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

    return resp(200,"users",usuarios_json,"teste")

#retorna um usuario especifico

#cadastrar usuario

#modificar usuario

#deletar usuario

def resp(status, n_cont, cont, sms = False):
    body = {}
    body[n_cont] = cont

    if(sms):
        body["mensagem"] = sms

    return Response(json.dumps(body), status = 200, mimetype = "application/json")

app.run()