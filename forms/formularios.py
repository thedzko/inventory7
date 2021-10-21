from flask_wtf import FlaskForm, form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email


class Login(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Usuario es obligartorio")], render_kw={"placeholder": "Username"})
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Password es obligatorio")], render_kw={"placeholder": "Password"})
    entrar = SubmitField("Entrar")


class Registro(FlaskForm):
    id = StringField("Nombre", validators=[
        DataRequired(message="id es obligatorio")], render_kw={"placeholder": "Identificación"})
    nombre = StringField("Nombre", validators=[
        DataRequired(message="Nombre es obligatorio")], render_kw={"placeholder": "Nombre"})
    username = StringField("Usuario", validators=[
        DataRequired(message="Usuario es obligatorio")], render_kw={"placeholder": "Username"})
    correo = StringField("Correo", validators=[
        DataRequired(message="Correo es obligatorio")], render_kw={"placeholder": "Correo Institucional"})
    password = PasswordField("Password", validators=[
        DataRequired(message="Password es obligatorio")], render_kw={"placeholder": "Contraseña"})
    perfil = SelectField("Perfiles", choices=[("administrador", "administrador"), ("usuario", "usuario")])
    
    registrar = SubmitField("Registrar")


class Productos(FlaskForm):
    identificador = StringField("Código", render_kw={"placeholder": "Identificador",})
    nombre = StringField("Nombre del Producto", render_kw={"placeholder": "Nombre del producto"})
    proveedores = StringField("Proveedores", render_kw={"placeholder": "Proveedores"})
    cantidad_disp = StringField("Cantidad disp.", render_kw={"placeholder": "Cantidad Disp."})
    cantidad_min = StringField("Cantidad min.", render_kw={"placeholder": "Cantidad Min."})
    descripcion = TextAreaField("Descripcion", render_kw={"placeholder": "Descripcion."})
    retail_price = StringField("Cantidad Disp.", render_kw={"placeholder": "Retail Price."})
    trade_price= StringField("Cantidad Min.", render_kw={"placeholder": "Trade Price."})

    enviar = SubmitField("Enviar", render_kw=({"onfocus":"cambiarRuta('/producto/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiarRuta('/producto/get')"}))
    eliminar = SubmitField("eliminar", render_kw=({"onfocus":"cambiarRuta('/producto/delete')"}))
    editar = SubmitField("Editar Información", render_kw=({"onfocus":"cambiarRuta('/producto/update')"}))

#---------------------------------------------------------------------

class Proveedores(FlaskForm):
    identificador = StringField("Código", render_kw={"placeholder": "Identificador",})
    nombre = StringField("Nombre", render_kw={"placeholder": "Nombre Proveedor"})
    correo = StringField("corre", render_kw={"placeholder": "Correo"})
    telefono = StringField("telefono.", render_kw={"placeholder": "Telefono."})
    celular = StringField("Celular.", render_kw={"placeholder": "Celular."})
    productos = TextAreaField("productos", render_kw={"placeholder": "Productos."})
    ubicacion = TextAreaField("ubicacion.", render_kw={"placeholder": "Ubicacion."})

    enviar = SubmitField("Enviar", render_kw=({"onfocus":"cambiarRuta('/proveedor/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiarRuta('/proveedor/get')"}))
    eliminar = SubmitField("eliminar", render_kw=({"onfocus":"cambiarRuta('/proveedor/delete')"}))
    editar = SubmitField("Editar Información", render_kw=({"onfocus":"cambiarRuta('/proveedor/update')"}))

#-------usuarios------------------------------------------------------------------
class Usuarios(FlaskForm):
    id = StringField("Nombre",  render_kw={"placeholder": "Identificación"})
    nombre = StringField("Nombre", render_kw={"placeholder": "Nombre"})
    username = StringField("Usuario", render_kw={"placeholder": "Username"})
    correo = StringField("Correo",  render_kw={"placeholder": "Correo Institucional"})
    password = PasswordField("Password", render_kw={"placeholder": "Contraseña"})
    perfil = SelectField("Perfiles", choices=[("administrador", "administrador"), ("usuario", "usuario")])

    enviar = SubmitField("Enviar", render_kw=({"onfocus":"cambiarRuta('/usuario/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiarRuta('/usuario/get')"}))
    eliminar = SubmitField("eliminar", render_kw=({"onfocus":"cambiarRuta('/usuario/delete')"}))
    editar = SubmitField("Editar Información", render_kw=({"onfocus":"cambiarRuta('/usuario/update')"}))