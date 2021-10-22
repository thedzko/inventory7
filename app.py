from flask import Flask, render_template, request, flash, session, redirect
import sqlite3
import os
from werkzeug.utils import escape
from forms.formularios import Login, Proveedores, Registro, Productos, Usuarios
import hashlib

app=Flask(__name__)
app.secret_key=os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def home():
    frm = Login()
    if frm.validate_on_submit():
        username= escape(frm.username.data)
        password= escape(frm.password.data)
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()
        with sqlite3.connect("inventario.db") as con:
            con.row_factory= sqlite3.Row
            cursor = con.cursor()
            cursor.execute ("SELECT * FROM usuario WHERE username=? AND password =?",[username, pass_enc])
            row=cursor.fetchone()
            if row:
                session['usuario'] = username
                session["perfil"] = row["perfil"]
                if session["perfil"] == "administrador":
                    return redirect ("/usuarios")
                elif session["perfil"] == "usuario":
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
        id=escape(frm.id.data)
        nombre=escape(frm.nombre.data)
        correo= escape(frm.correo.data)
        username=escape(frm.username.data)
        perfil=escape(frm.perfil.data)
        password=escape(frm.password.data)
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()

        #conecta a la base de datos
        with sqlite3.connect("inventario.db") as con:
            cursor = con.cursor() #manipular la base de datos
            cursor.execute("SELECT * FROM usuario WHERE username = ? OR id = ?", [username, id])
            
            # Si existe
            if cursor.fetchone():
                flash( "Usuario ya se encuentra registrado")
            else:
                #Prepara la sentencia SQL a ejecutar
                cursor.execute("INSERT INTO usuario (id, nombre, username, correo, perfil, password) VALUES(?,?,?,?,?,?)", [id, nombre, username, correo, perfil, pass_enc])
                #Ejecuta la sentencia SQL
                con.commit()
                flash( "guardado con exito")
               # return redirect("/")
    return render_template("registro.html", frm=frm)

#---------------Rutas--------------------------------------
@app.route("/productos", methods = ["GET", "POST"])
def prod():
    #if 'usuario' in session:
    if 'usuario' in session:
        producto = Productos()
        return render_template("producto.html", frm=producto)
    #return redirect("/")

@app.route("/proveedores", methods = ["GET", "POST"])
def prove():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    #if 'usuario' in session:
        proveedores = Proveedores()
        return render_template("proveedor.html", frm=proveedores)
    #return redirect("/")

@app.route("/usuarios", methods = ["GET", "POST"])
def usu():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        usuarios = Usuarios()
        return render_template("usuario.html", frm=usuarios)
    #return redirect("/")
#--------------------------------------------------------------------------------------------------

#----Producto-------------------------------------------------------------------------------------
@app.route("/producto/save", methods = ["POST"])
def prod_save():
    #if 'usuario' in session and session["perfil"]=="admministrador" :
    if 'usuario' in session:
        producto = Productos()
        nombre = escape(producto.nombre.data)
        proveedores = escape(producto.proveedores.data)
        cantidad_disp = escape(producto.cantidad_disp.data)
        cantidad_min = escape(producto.cantidad_min.data)
        descripcion = escape(producto.descripcion.data)
        retail_price= escape(producto.retail_price.data)
        trade_price = escape(producto.trade_price.data)
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
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        producto = Productos()
        identificador = escape(producto.identificador.data)
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
    

@app.route("/producto/update", methods=["POST"])
def prod_update():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        frm = Productos()
        nombre = frm.nombre.data
        proveedores = escape(frm.proveedores.data)
        cantidad_disp = escape(frm.cantidad_disp.data)
        cantidad_min = escape(frm.cantidad_min.data)
        descripcion = escape(frm.descripcion.data)
        retail_price = escape(frm.retail_price.data)
        trade_price = escape(frm.trade_price.data)
        identificador = escape(frm.identificador.data)
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
    return redirect("/")

@app.route("/producto/delete", methods = ["POST"])
def prod_delete():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        frm = Productos()
        identificador = escape(frm.identificador.data)
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
    return redirect("/")
#------------------------------------------------------------------------------------------------------
#-----proveedores--------------------------------------------------------------------------------------
@app.route("/proveedor/save", methods = ["POST"])
def prove_save():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        proveedor= Proveedores()
        nombre = escape(proveedor.nombre.data)
        correo = escape(proveedor.correo.data)
        telefono = escape(proveedor.telefono.data)
        celular = escape(proveedor.celular.data)        
        ubicacion = escape(proveedor.ubicacion.data)       
        productos= escape(proveedor.productos.data)        

        if len(nombre)>0 and len(nombre)<100:
            if len(nombre) > 0:
                with sqlite3.connect("inventario.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO proveedores (nombre, correo, telefono, celular, ubicacion, productos) VALUES (?,?,?,?,?,?)", [nombre, correo, telefono, celular, ubicacion, productos])
                    con.commit()
                    flash("Guardado con éxito")
            else:
                flash("debe digitar un proveedor")
        else:
            flash("El nombre debe estar ente 1 - 100 caracteres")

        return render_template("proveedor.html", frm=proveedor)

    return redirect("/")

@app.route("/proveedor/get", methods = ["POST"])
def prove_get():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        proveedor = Proveedores()
        identificador = proveedor.identificador.data
        if identificador:
            with sqlite3.connect("inventario.db") as con:
            #convierte la respuesta en un diccionario
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM proveedores  WHERE identificador = ?", [identificador])
                row = cur.fetchone()
                if row:
                    proveedor.nombre.data=row["nombre"]
                    proveedor.correo.data=row["correo"]
                    proveedor.telefono.data=row["telefono"]
                    proveedor.celular.data=row["celular"]
                    proveedor.productos.data=row["productos"]
                    proveedor.ubicacion.data=row["ubicacion"]

                else:
                    flash("producto no encontrado")
        else:
            flash("debe digitar el codigo del producto")

        return render_template("proveedor.html", frm=proveedor)
    return redirect("/")


@app.route("/proveedor/update", methods=["POST"])
def prove_update():
    #if 'usuario' in session and session["perfil"]=="admministrador":
    if 'usuario' in session:
        frm = Proveedores()
        nombre = escape(frm.nombre.data)
        correo = escape(frm.correo.data)
        telefono = escape(frm.telefono.data)
        celular = escape(frm.celular.data)
        productos = escape(frm.productos.data)
        ubicacion = escape(frm.ubicacion.data)
        identificador = escape(frm.identificador.data)

        if identificador and identificador.isnumeric():
            if nombre:
                with sqlite3.connect("inventario.db") as con:
                    cur = con.cursor()
                    cur.execute("UPDATE proveedores SET nombre = ?, correo =?, telefono=?, celular=?, productos=?, ubicacion=? WHERE identificador = ?", [nombre, correo, telefono, celular, productos, ubicacion, identificador])
                    con.commit()
                    if con.total_changes > 0:
                        flash("producto actualizado")
                    else:
                        flash("No se pudo actualizar Producto")
            else:
                flash("Debe digitar el Nombre")
        else:
            flash("Debe digitar un valor numerico")
        return render_template ("proveedor.html", frm=frm)
    #return redirect("/")

@app.route("/proveedor/delete", methods = ["POST"])
def prove_delete():
    if 'usuario' in session:
        frm = Proveedores()
        identificador = escape(frm.identificador.data)
        if identificador:
            with sqlite3.connect("inventario.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM proveedores WHERE identificador =?", [identificador])
                con.commit()
                if con.total_changes > 0:
                    flash("Producto Eliminado")
                else:
                    flash("Producto No se pudo Eliminar")
        else:
                flash("debe digitar el codigo de el producto")

        return render_template("proveedor.html", frm=frm)

#-----proveedores-----------------------------------------------------------------------------------------------------

#-----usuarios---------------------------------------------------------------------------------------------------------

@app.route("/usuario/save", methods = ["POST"])
def usu_save():
    if 'usuario' in session:
        usuario= Usuarios()
        id = escape(usuario.id.data) 
        nombre = escape(usuario.nombre.data)
        username = escape(usuario.username.data)
        correo = escape(usuario.correo.data)
        password = escape(usuario.password.data)        
        perfil = escape(usuario.perfil.data)
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()             

        if len(nombre)>0 and len(nombre)<100:
            if len(nombre) > 0:
                with sqlite3.connect("inventario.db") as con:
                    cursor = con.cursor()
                    cursor.execute("SELECT * FROM usuario WHERE username = ? OR id = ?", [username, id])
                    # Si existe
                    if cursor.fetchone():
                        flash( "Usuario ya se encuentra registrado")
                    else:
                        cursor.execute("INSERT INTO usuario (id, nombre, username, correo, password, perfil) VALUES (?,?,?,?,?,?)", [id, nombre, username, correo, pass_enc, perfil])
                        con.commit()
                        flash("Guardado con éxito")
            else:
                flash("debe digitar el nombre de usuario")
        else:
            flash("El nombre debe estar ente 1 - 100 caracteres")

        return render_template("usuario.html", frm=usuario)

    #return redirect("/")

@app.route("/usuario/get", methods = ["POST"])
def usu_get():
    if 'usuario' in session:
        usuario = Usuarios()
        id = escape(usuario.id.data)
        if id:
            with sqlite3.connect("inventario.db") as con:
            #convierte la respuesta en un diccionario
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM usuario  WHERE id = ?", [id])
                row = cur.fetchone()
                if row:
                   usuario.nombre.data = row["nombre"]
                   usuario.username.data = row["username"]
                   usuario.correo.data = row["correo"]
                   usuario.password.data = row["password"]
                   usuario.perfil.data = row["perfil"]

                else:
                    flash("usuario no encontrado")
        else:
            flash("debe digitar el codigo del usuario")

        return render_template("usuario.html", frm=usuario)
    #return redirect("/")

@app.route("/usuario/update", methods=["POST"])
def usu_update():
    if 'usuario' in session:
        frm = Usuarios()
        id = escape(frm.id.data)
        nombre = escape(frm.nombre.data)
        username = escape(frm.username.data)
        correo = escape(frm.correo.data)
        password = escape(frm.password.data)
        perfil = escape(frm.perfil.data)
        enc=hashlib.sha256(password.encode())
        pass_enc= enc.hexdigest()
    

        if id and id.isnumeric():
            if nombre:
                with sqlite3.connect("inventario.db") as con:
                    cursor = con.cursor()
                    cursor.execute("UPDATE usuario SET  nombre = ?, username=?, correo =?, password=?, perfil=? WHERE id= ?", [ nombre, username, correo, pass_enc, perfil, id])
                    con.commit()
                    if con.total_changes > 0:
                        flash("usuario actualizado")
                    else:
                        flash("No se pudo actualizar Usuario")
            else:
                flash("Debe digitar el nombre de usuario")
        else:
            flash("Debe digitar un valor numerico en id")

        return render_template ("usuario.html", frm=frm)


@app.route("/usuario/delete", methods = ["POST"])
def usu_delete():
    frm = Usuarios()
    id = escape(frm.id.data)
    if id:
        with sqlite3.connect("inventario.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM usuario WHERE id =?", [id])
            con.commit()
            if con.total_changes > 0:
                flash("Usario Eliminado")
            else:
                flash("usuario No se pudo Eliminar")
    else:
            flash("Debe digitar el id del producto")

    return render_template("usuario.html", frm=frm)

#-----usuarios---------------------------------------------------------------------------------------------------------



@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect ("/")

app.run(debug=True)