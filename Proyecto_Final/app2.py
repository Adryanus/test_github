from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Posteo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(255))
    titulo = db.Column(db.String(255))
    texto = db.Column(db.Text)

# Este método se ejecutará la primera vez
# cuando se construye la app.
with app.app_context():
    # Crear aquí la base de datos
    db.create_all()
    print("Base de datos generada")

# Endpoint login (/login)
@app.route('/login')
def login():
    return render_template('login.html')

# Endpoint de bienvenida o index (/)
@app.route('/')
def index():
    return render_template('blog.html')

# Endpoint post (/posteos/)
@app.route('/posteos/', methods=['GET', 'POST', 'DELETE'])
def posteos():
    if request.method == 'GET':
        usuario = request.args.get('usuario')
        posteos_usuario = Posteo.query.filter_by(usuario=usuario).order_by(Posteo.id.desc()).limit(3).all()

        datos = []
        for posteo in posteos_usuario:
            datos.append({"titulo": posteo.titulo, "texto": posteo.texto})

        return jsonify(datos)

    elif request.method == 'POST':
        usuario = request.args.get('usuario')
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')

        nuevo_posteo = Posteo(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(nuevo_posteo)
        db.session.commit()

        return Response(status=201)

    elif request.method == 'DELETE':
        usuario = request.args.get('usuario')
        Posteo.query.filter_by(usuario=usuario).delete()
        db.session.commit()

        return Response(status=200)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)