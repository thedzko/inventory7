from logging import debug
from flask import Flask, render_template, url_for

app = Flask (__name__)

@app.route('/')
def Inicio():
    return render_template ('login.html')

@app.route('/Productos')
def Productos():
    return render_template ('panelProductos.html')

@app.route('/Crear_Productos')
def crearProductos():
    return render_template ('producto.html')

@app.route('/Usuarios')
def Usuarios():
    return render_template ('/panelUsuarios.html')

@app.route('/Proveedores')
def Proveedores():
    return render_template ('panelProveedores.html')

@app.route('/Crear_Proveedor')
def crearProveedor():
    return render_template ('proveedor.html')

if __name__ == '__main__':
    app.run (debug = True)

