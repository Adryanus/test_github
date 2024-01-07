from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
from datetime import datetime
import traceback

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy()
db.init_app(app)

class Posteos(db.Model):
    __tablename__ = "posteos"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    usuario = db.Column(db.String)
    titulo = db.Column(db.String)
    texto = db.Column(db.Text)

@app.route("/login")
def login():
    try:
        return render_template('login.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/")
def index():
    try:
        return render_template('blog.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/posteos/", methods=['GET', 'POST','DELETE'])
def posteos():
    if request.method == 'GET':
        try:
            usuario = str(request.form.get('usuario')).lower()
            query = db.session.query(Posteos).filter_by(usuario = usuario).order_by(Posteos.id.desc()).limit(3).all()
            return render_template('posteos.html', posteos=query)
            datos = []
            for posteo in query:
                datos.append({"titulo": posteo.titulo, "texto": posteo.texto})
            return jsonify(datos)
        except:
            return jsonify({'trace': traceback.format_exc()})

    elif request.method == 'POST':
        try:
            usuario = str(request.form.get('usuario')).lower()
            if(usuario is None):
                 return Response(status=400)
            else:
                titulo = str(request.form.get('titulo'))
                texto = str(request.form.get('texto'))
                posteo = Posteos(usuario=usuario, titulo=titulo, texto=texto)
                db.session.add(posteo)
                db.session.commit()
                return Response(status=201)
        except:
             return jsonify({'trace': traceback.format_exc()})

    elif request.method == 'DELETE':
        usuario = request.args.get('usuario')
        Posteo.query.filter_by(usuario=usuario).delete()
        db.session.commit()
        return Response(status=200)        

with app.app_context():
    db.drop_all()
    db.create_all()
    
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)