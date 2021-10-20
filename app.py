from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
import os
from forms.formularios import Login, Registro,Productos
import hashlib

app=Flask(__name__)
app.secret_key=os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def home():
    frm = Login()
    if frm.validate_on_submit():
        username= frm.username.data
        password= frm.password.data
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor()
            cursor.execute ("SELECT username FROM usuario WHERE username=? AND password =?",[username, pass_enc])
            if cursor.fetchone():
                session['usuario'] = username
                return redirect ("/productos")
            else:
                flash("usuario no valido")

    return render_template("login.html", frm=frm)

#API para registrarse
@app.route("/registrarse", methods=["GET", "POST"])#ruta
def registrar():#enpoint
    frm= Registro()#instancia el clase Registro
    #valida los datos del formulario
    if frm.validate_on_submit():
        #captura los datos del formulario
        id=frm.id.data
        nombre=frm.nombre.data
        correo= frm.correo.data
        username=frm.username.data
        password=frm.password.data
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()

        #conecta a la base de datos
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor() #manipular la base de datos
            cursor.execute(
                "SELECT * FROM usuario WHERE username = ? OR id = ?", [username, id])
            
            # Si existe
            if cursor.fetchone():
                flash( "Usuario ya se encuentra registrado")
            else:
                #Prepara la sentencia SQL a ejecutar
                cursor.execute("INSERT INTO usuario (id, nombre, username, correo, password) VALUES(?,?,?,?,?)", [id, nombre, username, correo, pass_enc])
                #Ejecuta la sentencia SQL
                con.commit()
                flash( "guardado con exito")
               # return redirect("/")
    return render_template("registro.html", frm=frm)

@app.route("/productos", methods = ["GET", "POST"])
def prod():
    if 'usuario' in session:
        producto = Productos()
        return render_template("producto.html", frm=producto)
    return redirect("/")

@app.route("/producto/save", methods = ["POST"])
def prod_save():
    if 'usuario' in session:
        producto = Productos()
        nombre = producto.nombre.data
        proveedores = producto.proveedores.data
        cantidad_disp = producto.cantidad_disp.data
        cantidad_min = producto.cantidad_min.data
        descripcion = producto.descripcion.data
        retail_price= producto.retail_price.data
        trade_price = producto.trade_price.data
        if len(nombre)>0 and len(nombre)<100:
            if len(proveedores) > 0:
                with sqlite3.connect("inventario.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO productos (nombre,proveedores,cantidad_disp,cantidad_min,descripcion,retail_price,trade_price) VALUES (?,?,?,?,?,?,?)", [nombre, proveedores, cantidad_disp,cantidad_min, descripcion, retail_price, trade_price])
                    con.commit()
                    flash("Guardado con éxito")
            else:
                flash("debe digitar un proveedor")
        else:
            flash("El nombre debe estar ente 1 - 100 caracteres")

        return render_template("producto.html", frm=producto)

    return redirect("/")

@app.route("/producto/get", methods = ["POST"])
def prod_get():
    if 'usuario' in session:
        producto = Productos()
        identificador = producto.identificador.data
        if identificador:
            with sqlite3.connect("inventario.db") as con:
            #convierte la respuesta en un diccionario
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM productos  WHERE identificador = ?", [identificador])
                row = cur.fetchone()
                if row:
                    producto.nombre.data=row["nombre"]
                    producto.proveedores.data=row["proveedores"]
                    producto.cantidad_disp.data=row["cantidad_disp"]
                    producto.cantidad_min.data=row["cantidad_min"]
                    producto.descripcion.data=row["descripcion"]
                    producto.retail_price.data=row["retail_price"]
                    producto.trade_price.data=row["trade_price"]
                else:
                    flash("producto no encontrado")
        else:
            flash("debe digitar el codigo del producto")

        return render_template("producto.html", frm=producto)
    return redirect("/")

@app.route("/producto/update", methods=["POST"])
def prod_update():
    frm = Productos()
    nombre = frm.nombre.data
    proveedores = frm.proveedores.data
    cantidad_disp = frm.cantidad_disp.data
    cantidad_min = frm.cantidad_min.data
    descripcion = frm.descripcion.data
    retail_price = frm.retail_price.data
    trade_price = frm.trade_price.data
    identificador = frm.identificador.data
    if identificador and identificador.isnumeric():
        if nombre:
            with sqlite3.connect("inventario.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE productos SET nombre = ?, proveedores =?, cantidad_disp=?, cantidad_min=?, descripcion=?, retail_price=?, trade_price=? WHERE identificador = ?", [nombre,proveedores, cantidad_disp, cantidad_min, descripcion, retail_price, trade_price, identificador])
                con.commit()
                if con.total_changes > 0:
                    flash("producto actualizado")
                else:
                    flash("No se pudo actualizar Producto")
        else:
            flash("Debe digitar el Nombre")
    else:
        flash("Debe digitar un valor numerico")
    return render_template ("producto.html", frm=frm)

@app.route("/producto/delete", methods = ["POST"])
def prod_delete():
    frm = Productos()
    identificador = frm.identificador.data
    if identificador:
        with sqlite3.connect("inventario.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM productos WHERE identificador =?", [identificador])
            con.commit()
            if con.total_changes > 0:
                flash("Producto Eliminado")
            else:
                flash("Producto No se pudo Eliminar")
    else:
            flash("debe digitar el codigo de el producto")

    return render_template("producto.html", frm=frm)


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect ("/")

app.run(debug=True)