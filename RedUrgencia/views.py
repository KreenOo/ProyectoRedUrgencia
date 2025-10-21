from django.shortcuts import render, redirect
from datetime import datetime

pacientes_registrados = []

#Principal----------------------------------------------------------------------------------------------
def menu(request):
    return render(request, "principal/menu.html")

def login(request):
    error = ""
    if request.method == "POST":
        usu = request.POST.get("username", "")
        con = request.POST.get("password", "")

        if usu == "usu1" and con == "123":
            return redirect("menu_emisor")
        elif usu == "usu2" and con == "321":
            return redirect("menu_receptor")
        elif usu == "admin" and con == "qwer":
            return redirect("menu_admin")
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, "principal/login.html", {"error": error})

def contacto(request):
    return render(request, "principal/contacto.html")

def ayuda(request):
    return render(request, "principal/ayuda.html")

#Admin--------------------------------------------------------------------------------------------------
def menu_admin(request):
    return render(request, 'administrador/menu.html')

# Admin_usuario ------------------------------------------------------------------------------------------
def menu_admin_usuario(request):
    return render(request, 'administrador/usuarios/menu.html')

def admin_crear_usuario(request):
    if request.method == "POST":
        usuarios = request.session.get("usuarios_registrados", [])

        nuevo_id = 1
        if usuarios:
            nuevo_id = max(u["id"] for u in usuarios) + 1

        nuevo_usuario = {
            "id": nuevo_id,
            "nombre": request.POST.get("nombre", ""),
            "rut": request.POST.get("rut", ""),
            "correo": request.POST.get("correo", ""),
            "telefono": request.POST.get("telefono", ""),
            "rol": request.POST.get("rol", ""),
            "clave": request.POST.get("clave", ""),
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        usuarios.append(nuevo_usuario)
        request.session["usuarios_registrados"] = usuarios
        request.session.modified = True

        return redirect("listar_usuario")

    return render(request, 'administrador/usuarios/crear.html')

def admin_listar_usuario(request):
    usuarios = request.session.get("usuarios_registrados", [])
    query = request.GET.get("q", "").lower()

    if query:
        usuarios = [
            u for u in usuarios
            if query in u["nombre"].lower() or query in u["rut"].lower()
        ]

    return render(request, 'administrador/usuarios/listar.html', {"usuarios": usuarios, "query": query})

def admin_modificar_usuario(request, id):
    usuarios = request.session.get("usuarios_registrados", [])
    usuario = next((u for u in usuarios if u["id"] == id), None)

    if not usuario:
        return render(request, "administrador/usuarios/error.html", {"mensaje": "Usuario no encontrado"})

    if request.method == "POST":
        usuario["nombre"] = request.POST.get("nombre", usuario["nombre"])
        usuario["rut"] = request.POST.get("rut", usuario["rut"])
        usuario["correo"] = request.POST.get("correo", usuario["correo"])
        usuario["telefono"] = request.POST.get("telefono", usuario["telefono"])
        usuario["rol"] = request.POST.get("rol", usuario["rol"])
        usuario["clave"] = request.POST.get("clave", usuario["clave"])

        request.session["usuarios_registrados"] = usuarios
        request.session.modified = True

        return redirect("listar_usuario")

    return render(request, "administrador/usuarios/modificar.html", {"usuario": usuario})

def admin_eliminar_usuario(request, id):
    usuarios = request.session.get("usuarios_registrados", [])
    usuario = next((u for u in usuarios if u["id"] == id), None)

    if not usuario:
        return render(request, "administrador/usuarios/error.html", {"mensaje": "Usuario no encontrado"})

    if request.method == "POST":
        usuarios.remove(usuario)
        request.session["usuarios_registrados"] = usuarios
        request.session.modified = True
        return redirect("listar_usuario")

    return render(request, "administrador/usuarios/eliminar.html", {"usuario": usuario})

#Admin_paciente-----------------------------------------------------------------------------------------
def menu_admin_paciente(request):
    return render(request, 'administrador/pacientes/menu.html')

def admin_crear(request):
    if request.method == "POST":
        pacientes = request.session.get("pacientes_registrados", [])

        nuevo_id = 1
        if pacientes:
            nuevo_id = max(p["id"] for p in pacientes) + 1

        ahora = datetime.now()

        nuevo_paciente = {
            "id": nuevo_id,
            "nombre": request.POST.get("nombre", ""),
            "edad": request.POST.get("edad", ""),
            "rut": request.POST.get("rut", ""),
            "sexo": request.POST.get("sexo", ""),
            "direccion": request.POST.get("direccion", ""),
            "telefono": request.POST.get("telefono", ""),
            "estado_conciencia": request.POST.get("estado_conciencia", ""),
            "estado_pupilas": request.POST.get("estado_pupilas", ""),
            "alergias": request.POST.get("alergias", ""),
            "presion_Art": request.POST.get("presion_art", ""),
            "frecuencia_car": request.POST.get("frecuencia_car", ""),
            "frecuencia_res": request.POST.get("frecuencia_res", ""),
            "temperatura": request.POST.get("temperatura", ""),
            "saturacion_oxi": request.POST.get("saturacion_oxi", ""),
            "nivel_glu": request.POST.get("nivel_glu", ""),
            "sintomas": request.POST.get("sintomas", ""),
            "lesiones": request.POST.get("lesiones", ""),
            "observaciones": request.POST.get("observaciones", ""),
            #datos que no se ve
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M"),
            #"usuario": usu
        }

        pacientes.append(nuevo_paciente)
        request.session["pacientes_registrados"] = pacientes
        request.session.modified = True

        return redirect("listar_admin")

    return render(request, "administrador/pacientes/crear.html")

def admin_listar(request):
    pacientes = request.session.get("pacientes_registrados", [])
    query = request.GET.get("q", "").lower()

    if query:
        pacientes = [p for p in pacientes if query in p["nombre"].lower() or query in p["rut"].lower()]
    
    return render(request, "administrador/pacientes/listar.html", {"pacientes": pacientes, "query": query})

def admin_detalle(request, id):
    paciente = None
    pacientes = request.session.get("pacientes_registrados", [])
    for p in pacientes:
        if p["id"] == id:
            paciente = p
            break
    if paciente is None:
        return render(request, 'administrador/pacientes/detalle.html', {"error": "Paciente no encontrado"})
    return render(request, 'administrador/pacientes/detalle.html', {"paciente": paciente})

def admin_modificar(request, id):
    pacientes = request.session.get("pacientes_registrados", [])
    paciente = next((p for p in pacientes if p["id"] == id), None)

    if not paciente:
        return render(request, "administrador/pacientes/error.html", {"mensaje": "Paciente no encontrado"})

    if request.method == "POST":
        paciente["nombre"] = request.POST.get("nombre", paciente["nombre"])
        paciente["edad"] = request.POST.get("edad", paciente["edad"])
        paciente["rut"] = request.POST.get("rut", paciente["rut"])
        paciente["sexo"] = request.POST.get("sexo", paciente["sexo"])
        paciente["direccion"] = request.POST.get("direccion", paciente["direccion"])
        paciente["telefono"] = request.POST.get("telefono", paciente["telefono"])
        paciente["estado_conciencia"] = request.POST.get("estado_conciencia", paciente["estado_conciencia"])
        paciente["estado_Pupilas"] = request.POST.get("estado_pupilas", paciente["estado_pupilas"])
        paciente["alergias"] = request.POST.get("alergias", paciente["alergias"])
        paciente["presion_art"] = request.POST.get("presion_art", paciente["presion_art"])
        paciente["frecuencia_car"] = request.POST.get("frecuencia_car", paciente["frecuencia_car"])
        paciente["frecuencia_res"] = request.POST.get("frecuencia_res", paciente["frecuencia_res"])
        paciente["temperatura"] = request.POST.get("temperatura", paciente["temperatura"])
        paciente["saturacion_oxi"] = request.POST.get("saturacion_oxi", paciente["saturacion_oxi"])
        paciente["nivel_glu"] = request.POST.get("nivel_glu", paciente["nivel_glu"])
        paciente["sintomas"] = request.POST.get("sintomas", paciente["sintomas"])
        paciente["lesiones"] = request.POST.get("lesiones", paciente["lesiones"])
        paciente["observaciones"] = request.POST.get("observaciones", paciente["observaciones"])

        request.session["pacientes_registrados"] = pacientes
        request.session.modified = True

        return redirect("listar_admin")

    return render(request, "administrador/pacientes/modificar.html", {"paciente": paciente})


def admin_eliminar(request, id):
    pacientes = request.session.get("pacientes_registrados", [])
    paciente = next((p for p in pacientes if p["id"] == id), None)

    if not paciente:
        return render(request, "administrador/pacientes/error.html", {"mensaje": "Paciente no encontrado"})

    if request.method == "POST":
        pacientes.remove(paciente)
        request.session["pacientes_registrados"] = pacientes
        request.session.modified = True
        return redirect("listar_admin")

    return render(request, "administrador/pacientes/eliminar.html", {"paciente": paciente})

#Emisor-------------------------------------------------------------------------------------------------
def menu_emisor(request):
    return render(request, "emisor/menu.html")

def emisor(request):
    if request.method == "POST":
        pacientes = request.session.get("pacientes_registrados", [])

        nuevo_id = 1
        if pacientes:
            nuevo_id = max(p["id"] for p in pacientes) + 1

        ahora = datetime.now()

        alergias_radio = request.POST.get("alergias_radio", "Ninguna")
        alergias = request.POST.get("alergias", "") if alergias_radio == "Otra" else "Ninguna"

        nuevo_paciente = {
            "id": nuevo_id,
            "nombre": request.POST.get("nombre", ""),
            "edad": request.POST.get("edad", ""),
            "rut": request.POST.get("rut", ""),
            "sexo": request.POST.get("sexo", ""),
            "direccion": request.POST.get("direccion", ""),
            "telefono": request.POST.get("telefono", ""),
            "estado_conciencia": request.POST.get("estado_conciencia", ""),
            "estado_pupilas": request.POST.get("estado_pupilas", ""),
            "alergias": request.POST.get("alergias", ""),
            "presion_Art": request.POST.get("presion_art", ""),
            "frecuencia_car": request.POST.get("frecuencia_car", ""),
            "frecuencia_res": request.POST.get("frecuencia_res", ""),
            "temperatura": request.POST.get("temperatura", ""),
            "saturacion_oxi": request.POST.get("saturacion_oxi", ""),
            "nivel_glu": request.POST.get("nivel_glu", ""),
            "sintomas": request.POST.get("sintomas", ""),
            "lesiones": request.POST.get("lesiones", ""),
            "observaciones": request.POST.get("observaciones", ""),
            #datos que no se ve
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M"),
            #"usuario": usu
        }

        pacientes.append(nuevo_paciente)
        request.session["pacientes_registrados"] = pacientes
        request.session.modified = True

        return redirect("emisor")

    else:
        pacientes = request.session.get("pacientes_registrados", [])
        ultimo = pacientes[-1] if pacientes else None

        return render(request, "emisor/crear.html", {"paciente": ultimo})

def editar_emisor(request, id):
    pacientes = request.session.get("pacientes_registrados", [])
    paciente = next((p for p in pacientes if p["id"] == id), None)

    if not paciente:
        return redirect("emisor")

    if request.method == "POST":
        paciente["nombre"] = request.POST.get("nombre", paciente["nombre"])
        paciente["edad"] = request.POST.get("edad", paciente["edad"])
        paciente["rut"] = request.POST.get("rut", paciente["rut"])
        paciente["sexo"] = request.POST.get("sexo", paciente["sexo"])
        paciente["direccion"] = request.POST.get("direccion", paciente["direccion"])
        paciente["telefono"] = request.POST.get("telefono", paciente["telefono"])
        paciente["estado_conciencia"] = request.POST.get("estado_conciencia", paciente["estado_conciencia"])
        paciente["estado_Pupilas"] = request.POST.get("estado_pupilas", paciente["estado_pupilas"])
        paciente["alergias"] = request.POST.get("alergias", paciente["alergias"])
        paciente["presion_art"] = request.POST.get("presion_art", paciente["presion_art"])
        paciente["frecuencia_car"] = request.POST.get("frecuencia_car", paciente["frecuencia_car"])
        paciente["frecuencia_res"] = request.POST.get("frecuencia_res", paciente["frecuencia_res"])
        paciente["temperatura"] = request.POST.get("temperatura", paciente["temperatura"])
        paciente["saturacion_oxi"] = request.POST.get("saturacion_oxi", paciente["saturacion_oxi"])
        paciente["nivel_glu"] = request.POST.get("nivel_glu", paciente["nivel_glu"])
        paciente["sintomas"] = request.POST.get("sintomas", paciente["sintomas"])
        paciente["lesiones"] = request.POST.get("lesiones", paciente["lesiones"])
        paciente["observaciones"] = request.POST.get("observaciones", paciente["observaciones"])

        request.session["pacientes_registrados"] = pacientes
        request.session.modified = True

        return redirect("emisor")

    return render(request, "emisor/editar.html", {"paciente": paciente})

def lista_emisor(request):
    pacientes = request.session.get("pacientes_registrados", [])
    query = request.GET.get("q", "").lower()

    if query:
        pacientes = [p for p in pacientes if query in p["nombre"].lower() or query in p["rut"].lower()]
    
    return render(request, "emisor/lista.html", {"pacientes": pacientes, "query": query})

#Receptor-----------------------------------------------------------------------------------------------
def menu_receptor(request):
    return render(request, "receptor/menu.html")

def receptor(request):
    pacientes = request.session.get("pacientes_registrados", [])
    query = request.GET.get("q", "").lower()

    if query:
        pacientes = [p for p in pacientes if query in p["nombre"].lower() or query in p["rut"].lower()]
    
    return render(request, "receptor/listar.html", {"pacientes": pacientes, "query": query})

def seguimiento(request):
    pacientes = request.session.get("pacientes_registrados", [])
    ambulancias = [
        {
            "id": 1,
            "conductor": "Pedro Salas",
            "patente": "AB1234",
            "ubicacion": "Av. Libertad 123",
            "estado": "Activa"
        },
        {
            "id": 2,
            "conductor": "Lucía Muñoz",
            "patente": "XY9876",
            "ubicacion": "Calle Falsa 456",
            "estado": "Activa"
        },
    ]
    return render(request, "receptor/seguimiento.html", {
        "pacientes": pacientes[-5:],
        "ambulancias": ambulancias
    })



def detalles_paciente(request, id):
    paciente = None
    pacientes = request.session.get("pacientes_registrados", [])
    for p in pacientes:
        if p["id"] == id:
            paciente = p
            break
    if paciente is None:
        return render(request, 'receptor/detalle.html', {"error": "Paciente no encontrado"})
    return render(request, 'receptor/detalle.html', {"paciente": paciente})

def buscar_paciente(request):
    pacientes = request.session.get("pacientes_registrados", [])
    query = request.GET.get("q", "").lower()
    fecha_inicio = request.GET.get("fecha_inicio", "")
    fecha_fin = request.GET.get("fecha_fin", "")
    hora_inicio = request.GET.get("hora_inicio", "")
    hora_fin = request.GET.get("hora_fin", "")
    sexo = request.GET.get("sexo", "")
    sin_nombre = request.GET.get("sin_nombre", "")
    sin_rut = request.GET.get("sin_rut", "")
    edad_min = request.GET.get("edad_min")
    edad_max = request.GET.get("edad_max")

    if query:
        pacientes = [
            p for p in pacientes
            if query in p.get("nombre", "").lower() or query in p.get("rut", "").lower()
        ]

    if fecha_inicio:
        pacientes = [p for p in pacientes if p.get("fecha", "") >= fecha_inicio]

    if fecha_fin:
        pacientes = [p for p in pacientes if p.get("fecha", "") <= fecha_fin]

    if hora_inicio:
        pacientes = [p for p in pacientes if p.get("hora", "") >= hora_inicio]

    if hora_fin:
        pacientes = [p for p in pacientes if p.get("hora", "") <= hora_fin]

    if sexo:
        pacientes = [p for p in pacientes if p.get("sexo", "") == sexo]

    if sin_nombre:
        pacientes = [p for p in pacientes if not p.get("nombre")]

    if sin_rut:
        pacientes = [p for p in pacientes if not p.get("rut")]

    if edad_min:
        try:
            edad_min = int(edad_min)
            pacientes = [p for p in pacientes if p.get("edad") and int(p["edad"]) >= edad_min]
        except ValueError:
            pass

    if edad_max:
        try:
            edad_max = int(edad_max)
            pacientes = [p for p in pacientes if p.get("edad") and int(p["edad"]) <= edad_max]
        except ValueError:
            pass

    return render(request, "receptor/buscar.html", {"pacientes": pacientes})
