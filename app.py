from re import escape
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1849@localhost/crud'

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
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
@app.route("/usuario/<id>",methods=["GET"])
def ret_user(id):
    try:
        usuario_objeto = Usuario.query.filter_by(id=id).first()
        usuario_json = usuario_objeto.to_json()
        return resp(200,"user",usuario_json,"ok")
    except Exception as e:
        print(e)
        return resp(400,"user",{},"Usuario nao existe")

#cadastrar usuario
@app.route("/cadastro",methods = ["POST"])
def new_user():
    body = request.get_json()

    try:
        usuario_objeto = Usuario(nome = body["nome"],email = body["email"])
        db.session.add(usuario)
        db.session.commit()
        return resp(201,"user",usuario_objeto.to_json(),"Usuario cadastrado")
    except Exception as e:
        print(e)
        return resp(400,"user",{},"Erro no cadastrado")


#modificar usuario
@app.route("/usuario/<id>",methods=["PUT"])
def edit(id):
    usuario_objeto = Usuario.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if("nome" in body):
            usuario_objeto.nome = body["nome"]
        if("email" in body):
            usuario_objeto.email = body["email"]
        db.session.add(usuario_objeto)
        db.session.commit()
        return resp(200,"user",usuario_objeto.to_json(),"Usuario atualizado")
    except Exception as e:
        print(e)
        return resp(400,"user",{},"Erro ao atualizar")


#deletar usuario

def resp(status, n_cont, cont, sms = False):
    body = {}
    body[n_cont] = cont

    if(sms):
        body["mensagem"] = sms

    return Response(json.dumps(body), status = 200, mimetype = "application/json")

app.run()