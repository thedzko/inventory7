var eliminando;
function cambiarRuta(ruta) {
    formulario = document.getElementById("formulario");
    formulario.action = ruta;
    eliminando = false;
    if (ruta=="/producto/delete"){
        eliminando =true;

    }
}

function confirmarEliminacion(){
    if (eliminando){
        let resp = confirm("realmente desea eliminar el registro?");
        return resp;
    }
    return true;
}