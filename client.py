from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.json_util import dumps, ObjectId
from dotenv import dotenv_values
import bcrypt



try:
    env = dotenv_values(".env")
    db = MongoClient(env["MONGO_URI"])
    usuarios = db.catalogo.usuario
    productos = db.catalogo.producto
    print("Conexión existosa a la Base de datos en la nube")
except ConnectionFailure:
    print("Error al conectar con la Base de datos en la nube")


app = Flask(__name__)

app.secret_key = env["secretky"]

sal = bcrypt.gensalt()


@app.route('/')
def main():
    mostrador = productos.find()
    if 'usr' in session:
        btn_primarios = 'hidden'
        btn_especiales = ''

    else:
        btn_primarios = ''
        btn_especiales = 'hidden'

    return render_template('main.html',mostrador=mostrador, btn_primarios=btn_primarios,btn_especiales=btn_especiales)


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        correo = request.form['correo']
        password = request.form['password']
        password = password.encode()
        password = bcrypt.hashpw(password,sal)
        usr = usuarios.find_one({"correo":correo, 'password': password})
        if usr:
            session['usr'] = correo
            session['usr_name'] = usr['nombre']
            return redirect('/')

        else: 
            return render_template('login.html',alerta = "/static/js/usuario_no_encontrado.js")

    return render_template('login.html')


@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        correo = request.form['correo']
        password = request.form['password']
        password = password.encode()
        password = bcrypt.hashpw(password,sal)
        nombre = request.form['nombre']
        usr = usuarios.find_one({"correo":correo})
        if usr:
            return render_template('signup.html',alerta = "/static/js/usuario_registrado.js")

        else: 
            id = usuarios.insert_one({"nombre":nombre,"correo":correo, "password":password})
            return redirect('/')
    return render_template('signup.html')    


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/mis_productos')
def mis_productos():
    if 'usr' in session:
        usr = usuarios.find({'correo':session['usr']})
        for x in usr:
            id_cliente=x['_id']
        mostrador = productos.find({'id_cliente':str(id_cliente)})
        return render_template('mis_productos.html',mostrador=mostrador, username=session['usr_name'])

    else:
        return render_template('login.html',alerta = "/static/js/no_login.js")


@app.route('/eliminar', methods=["GET","POST"])
def eliminar():
    if request.method == "POST":
        _idproducto = request.form['_idproducto']
        productos.delete_one({'_id': ObjectId(_idproducto)})
        return redirect('/mis_productos')

    return redirect('/mis_productos')


@app.route('/editar',methods=["GET","POST"])
def editar():
    if 'usr' in session:
        if request.method == "POST":
            producto = request.form['producto']
            tipo = request.form['tipo']
            precio = request.form['precio']
            _idproducto = request.form['_idproducto']
            id_cliente = request.form['id_cliente']
            productos.update({'_id':ObjectId(_idproducto)},{'id_cliente': id_cliente, 'producto': producto, 'tipo': tipo, 'precio': precio})
            return redirect('/mis_productos')

        elif request.method == "GET":
            _idproducto = request.args.get('_idproducto')
            mostrador = productos.find({'_id':ObjectId(_idproducto)})
            return render_template('editar.html', mostrador=mostrador, username=session['usr_name'])

    else:
        return render_template('login.html',alerta = "/static/js/no_login.js")


@app.route('/add_producto',methods=["GET","POST"])
def add_producto():
    if 'usr' in session:
        if request.method == "POST":
            producto = request.form['producto']
            tipo = request.form['tipo']
            precio = request.form['precio']
            usuario = usuarios.find_one({'correo':session['usr']})
            productos.insert_one({'id_cliente':str(usuario['_id']),'producto':producto, 'tipo':tipo, 'precio':precio})
            return redirect('/mis_productos')

        return render_template('add_producto.html', username=session['usr_name'])

    else:
        return render_template('login.html',alerta = "/static/js/no_login.js")


if __name__ == '__main__':
    print("Desactive el CORTAFUEGOS si no lo ha hecho")
    app.run(host='0.0.0.0', port=80, debug=False)
