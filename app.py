from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson.json_util import dumps, ObjectId
from dotenv import dotenv_values
import bcrypt


# Conexion a la báse de datos
try:
    env = dotenv_values(".env")
    db = MongoClient(env["MONGO_URI"])
    usuarios = db.catalogo.usuario  
    productos = db.catalogo.producto
    print("Conexión existosa a la Base de datos en la nube")
except ConnectionFailure:
    print("Error al conectar con la Base de datos en la nube")


app = Flask(__name__)

app.secret_key = env["secretky"] #Llave secreta para ejecutar session cuyo valor se encuentra en el archivo .env

sal = bcrypt.gensalt()


# Ruta principal que muestra el catalogo completo y dependiendo de si se ha iniciado sesión
# oculta o muestra ciertas partes del front
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


# Ruta para iniciar sesión
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        correo = request.form['correo']
        password = request.form['password']
        password = password.encode()    #Codifica la contraseña
        password = bcrypt.hashpw(password,sal)  #Hashea la contraseña
        usr = usuarios.find_one({"correo":correo, 'password': password}) #Busca coinsidencias de correo y contraseña en la DB
        if usr:     #Si encuentra las coincidencias anteriores inicia una sesión y redirecciona a la página principal
            session['usr'] = correo
            session['usr_name'] = usr['nombre']
            return redirect('/')

        else:       #si no encuentra las coincidencias arroja una alerta
            return render_template('login.html',alerta = "/static/js/usuario_no_encontrado.js")

    return render_template('login.html')


# Ruta para registrar un nuevo usuario
@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        correo = request.form['correo']
        password = request.form['password']
        password = password.encode()    #Codifica la contraseña
        password = bcrypt.hashpw(password,sal)  #Hashea la contraseña
        nombre = request.form['nombre']
        usr = usuarios.find_one({"correo":correo})  #Busca si el correo ya esta registrado
        if usr:     #Si el correo ya fue registrado envía una alerta
            return render_template('signup.html',alerta = "/static/js/usuario_registrado.js")

        else:       #Al no encontrar registrado el correo procede a guardar la información en la base de datos
            id = usuarios.insert_one({"nombre":nombre,"correo":correo, "password":password})
            return redirect('/')
    return render_template('signup.html')    


# Ruta para cerrar sesión
# Al acceder a esta ruta se borran los datos de sesión y redirecciona a la página principal
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Ruta para ver los productos que ah registrado un usuario
@app.route('/mis_productos')
def mis_productos():
    if 'usr' in session:    #Si la sesión está activa busca los productos con los datos de la sesión actual
        usr = usuarios.find({'correo':session['usr']})
        for x in usr:
            id_cliente=x['_id']     #Accede al _id que tiene el usuario en sesión
        mostrador = productos.find({'id_cliente':str(id_cliente)})  #Busca los productos que tienen como "id_cliente" el "_id" del usuario en sesión
        return render_template('mis_productos.html',mostrador=mostrador, username=session['usr_name'])  #Envía los datos al front para que sean renderizados

    else:                   #Si no hay sesion activa envía una alerta y redirecciona a la página de inicio de sesión
        return render_template('login.html',alerta = "/static/js/no_login.js")


# Ruta para eliminar un producto registrado
# Mediante el metodo post recibe la información del producto a eliminar y lo elimina de la base de datos
@app.route('/eliminar', methods=["GET","POST"])
def eliminar():
    if request.method == "POST":
        _idproducto = request.form['_idproducto']
        productos.delete_one({'_id': ObjectId(_idproducto)})
        return redirect('/mis_productos')

    return redirect('/mis_productos')


# Ruta para editar un producto registrado
@app.route('/editar',methods=["GET","POST"])
def editar():
    if 'usr' in session:    #Si hay una sesión iniciada
        if request.method == "POST":
            #Recibe atravéz de un metodo post los cambios realizados y actualiza
            #el documento en la base de datos
            producto = request.form['producto']
            tipo = request.form['tipo']
            precio = request.form['precio']
            _idproducto = request.form['_idproducto']
            id_cliente = request.form['id_cliente']
            productos.update({'_id':ObjectId(_idproducto)},{'id_cliente': id_cliente, 'producto': producto, 'tipo': tipo, 'precio': precio})
            return redirect('/mis_productos')

        elif request.method == "GET":
            #Recibe por medio del metodo get el "_id" del producto a editar, lo busca en la base de datos
            #y proporciona la información del producto al front para su posterior edición
            _idproducto = request.args.get('_idproducto')
            mostrador = productos.find({'_id':ObjectId(_idproducto)})
            return render_template('editar.html', mostrador=mostrador, username=session['usr_name'])

    else:
        return render_template('login.html',alerta = "/static/js/no_login.js")


# Ruta para registra un nuevo producto
@app.route('/add_producto',methods=["GET","POST"])
def add_producto():
    if 'usr' in session:        #Si hay una sesión iniciada
        if request.method == "POST":
            #Al recibir una petición post obtiene del front la información del nuevo producto
            #Busca el "_id" del usuario en sesión y posteriormente registra el producto con el "id_cliente"
            #que es la clave que realiza la referencia de usuario-producto
            producto = request.form['producto']
            tipo = request.form['tipo']
            precio = request.form['precio']
            usuario = usuarios.find_one({'correo':session['usr']})
            productos.insert_one({'id_cliente':str(usuario['_id']),'producto':producto, 'tipo':tipo, 'precio':precio})
            return redirect('/mis_productos')

        return render_template('add_producto.html', username=session['usr_name']) #Envía el formulario en blanco

    else:               #Al no haber sesión activa manda una alerta y redirecciona al login
        return render_template('login.html',alerta = "/static/js/no_login.js")


if __name__ == '__main__':
    print("Desactive el CORTAFUEGOS si no lo ha hecho")
    app.run(host='0.0.0.0', port=80, debug=False)
