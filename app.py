from sqlite3.dbapi2 import connect
from flask import Flask, render_template, url_for, request, redirect
from datetime import date, datetime
# Importación SQLite
import sqlite3

app = Flask (__name__)

# Conectar base de datos SQLite
def sql_connection():
    connectDB = sqlite3.connect('inventory.db')
    return connectDB
# Rutas y Funciones

## USUARIOS
# GET (LIST) - USER
@app.route('/', methods=['GET'])
def panelUsuarios():
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute("SELECT * FROM users")
    #Nueva variable para que traiga todo lo de la tabla
    user_data = cur.fetchall()
    return render_template('panelUsuarios.html', users = user_data)

# POST - USER
@app.route('/newUser', methods=['GET','POST'])
def crearUsuario():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        user_join = datetime.now()
        user_age = datetime.now()
        connectDB = sql_connection()
        cur = connectDB.cursor()
        statement = "INSERT INTO users (username, role, user_join, user_age) VALUES (?, ?, ?, ?)"
        cur.execute(statement, [username, role, user_join, user_age])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelUsuarios'))
    else:
        return render_template('crearUsuario.html')

# GET(SHOW) - USER
@app.route('/showuser/<int:user_id>', methods=['GET'])
def verUsuario(user_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM users WHERE user_id=?"
    cur = cur.execute(consulta, [user_id])
    user_data = cur.fetchone()
    cur.close
    return render_template('verUsuario.html', users = user_data)

# EDIT - USER
@app.route('/edituser/<int:user_id>', methods=['GET', 'POST'])
def editarUsuario(user_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM users WHERE user_id=?"
    cur = cur.execute(consulta, [user_id])
    user_data = cur.fetchone()
    cur.close
    return render_template('editarUsuario.html', users = user_data)

# UPDATE - USER
@app.route('/updateuser/<int:user_id>', methods=['GET', 'POST'])
def actualizarUsuario(user_id):
    if request.method == 'POST':
        connectDB = sql_connection()
        username = request.form['username']
        role = request.form['role']
        cur = connectDB.cursor()
        consulta = "UPDATE users SET username = ?, role = ? WHERE user_id = ?"
        cur.execute(consulta, [username, role, user_id])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelUsuarios'))

# DELETE - USER
@app.route('/deleteuseruser/<int:user_id>', methods=['GET', 'POST'])
def borrarUsuario(user_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute('DELETE FROM users WHERE user_id={0}'.format(user_id))
    connectDB.commit()
    return redirect(url_for('panelUsuarios'))


## PRODUCTOS
# GET (LIST) - PRODUCT
@app.route('/productos/', methods=['GET'])
def panelProductos():
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute("SELECT * FROM products")
    product_data = cur.fetchall()
    return render_template('panelProductos.html', products = product_data)

# POST - PRODUCT
@app.route('/newProduct/', methods=['GET','POST'])
def crearProducto():
    if request.method == 'POST':
        productname = request.form['productname']
        providers = request.form['providers']
        available_amount = request.form['available_amount']
        least_amount = request.form['least_amount']
        product_description = request.form['product_description']
        product_retail = request.form['product_retail']
        product_trade = request.form['product_trade']
        connectDB = sql_connection()
        cur = connectDB.cursor()
        statement = "INSERT INTO products (productname, providers, available_amount, least_amount, product_description, product_retail, product_trade) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cur.execute(statement, [productname, providers, available_amount, least_amount, product_description, product_retail, product_trade])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelProductos'))
    else:
        return render_template('crearProducto.html')

# GET(SHOW) - PRODUCT
@app.route('/showproduct/<int:product_id>', methods=['GET'])
def verProducto(product_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM products WHERE product_id=?"
    cur = cur.execute(consulta, [product_id])
    product_data = cur.fetchone()
    cur.close
    return render_template('verProducto.html', products = product_data)

# EDIT - PRODUCT
@app.route('/editproduct/<int:product_id>', methods=['GET', 'POST'])
def editarProducto(product_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM products WHERE product_id=?"
    cur = cur.execute(consulta, [product_id])
    product_data = cur.fetchone()
    cur.close
    return render_template('editarProducto.html', products = product_data)

# UPDATE - PRODUCT
@app.route('/updateproduct/<int:product_id>', methods=['GET', 'POST'])
def actualizarProducto(product_id):
    if request.method == 'POST':
        connectDB = sql_connection()
        productname = request.form['productname']
        providers = request.form['providers']
        available_amount = request.form['available_amount']
        least_amount = request.form['least_amount']
        product_description = request.form['product_description']
        product_retail = request.form['product_retail']
        product_trade = request.form['product_trade']
        cur = connectDB.cursor()
        consulta = "UPDATE products SET productname = ?, providers = ?, available_amount = ?, least_amount = ?, product_description = ?, product_retail = ?, product_trade = ? WHERE product_id = ?"
        cur.execute(consulta, [productname, providers, available_amount, least_amount, product_description, product_retail, product_trade, product_id])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelProductos'))

# DELETE - PRODUCT
@app.route('/deleteproduct/<int:product_id>/', methods=['GET', 'POST'])
def borrarProducto(product_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute('DELETE FROM products WHERE product_id={0}'.format(product_id))
    connectDB.commit()
    return redirect(url_for('panelProductos'))


## PROVEEDORES
# GET (LIST) - PROVIDER
@app.route('/proveedores/', methods=['GET'])
def panelProveedores():
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute("SELECT * FROM providers")
    provider_data = cur.fetchall()
    return render_template('panelProveedores.html', providers = provider_data)

# POST - PROVIDER
@app.route('/newProvider/', methods=['GET','POST'])
def crearProveedor():
    if request.method == 'POST':
        providername = request.form['providername']
        products = request.form['products']
        phone = request.form['phone']
        celular = request.form['celular']
        email = request.form['email']
        location = request.form['location']        
        connectDB = sql_connection()
        cur = connectDB.cursor()
        statement = "INSERT INTO providers (providername, products, phone, celular, email, location) VALUES (?, ?, ?, ?, ?, ?)"
        cur.execute(statement, [providername, products, phone, celular, email, location])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelProveedores'))
    else:
        return render_template('crearProveedor.html')

# GET(SHOW) - PROVIDER
@app.route('/showprovider/<int:provider_id>', methods=['GET'])
def verProveedor(provider_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM providers WHERE provider_id=?"
    cur = cur.execute(consulta, [provider_id])
    provider_data = cur.fetchone()
    cur.close
    return render_template('verProveedor.html', providers = provider_data)

# EDIT - PROVIDER
@app.route('/editprovider/<int:provider_id>', methods=['GET', 'POST'])
def editarProveedor(provider_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    consulta = "SELECT * FROM providers WHERE provider_id=?"
    cur = cur.execute(consulta, [provider_id])
    provider_data = cur.fetchone()
    cur.close
    return render_template('editarProveedor.html', providers = provider_data)

# UPDATE - PROVIDER
@app.route('/updateprovider/<int:provider_id>', methods=['GET', 'POST'])
def actualizarProveedor(provider_id):
    if request.method == 'POST':
        connectDB = sql_connection()
        providermame = request.form['providermame']
        products = request.form['products']
        phone = request.form['phone']
        celular = request.form['celular']
        email = request.form['email']
        location = request.form['location']
        cur = connectDB.cursor()
        consulta = "UPDATE providers SET providermame = ?, products = ?, phone = ?, celular = ?, email = ?, location = ? WHERE provider_id = ?"
        cur.execute(consulta, [providermame, products, phone, celular, email, location, provider_id])
        connectDB.commit()
        cur.close
        return redirect(url_for('panelProveedores'))

# DELETE - PROVIDER
@app.route('/deleteprovider/<int:provider_id>/', methods=['GET', 'POST'])
def borrarProveedor(provider_id):
    connectDB = sql_connection()
    cur = connectDB.cursor()
    cur.execute('DELETE FROM providers WHERE provider_id={0}'.format(provider_id))
    connectDB.commit()
    return redirect(url_for('panelProveedores'))

if __name__ == '__main__':
    app.debug = True
    app.run()