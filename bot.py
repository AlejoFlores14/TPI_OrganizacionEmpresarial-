"""
Logica del chatbot
"""
import json

from datetime import datetime
ARCHIVO = "datos.json"
def cargar_datos():
    """
    Carga los datos del archivo JSON
    """
    with open(ARCHIVO, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    return datos
def guardar_datos(datos):
    """
    Guarda los datos en el archivo JSON
    """
    with open(ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4)

def validar_fecha(fecha):
    """
    Valida que la fecha sea correcta
    """
    try:
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False
def fecha_fin_valida(inicio,fin):
    """
    Valida que la fecha de fin sea mayor a la de inicio
    """
    valido_inicio = datetime.strptime(inicio, '%d/%m/%Y')
    valido_fin = datetime.strptime(fin, '%d/%m/%Y')
    return valido_fin > valido_inicio

def calcular_dias(inicio,fin):
    """
    Calcula los dias entre dos fechas
    """
    valido_inicio = datetime.strptime(inicio, '%d/%m/%Y')
    valido_fin = datetime.strptime(fin, '%d/%m/%Y')
    return (valido_fin - valido_inicio).days

def iniciar_bot():
    """
    Inicia el bot
    """
    print("Bot iniciado")
    print("Cargando datos...")
    print("="*30)
    datos = cargar_datos()
    while True:
        legajo = input("Ingrese el legajo del empleado: ").strip().upper()
        if legajo in datos["empleados"]:
            empleado = datos["empleados"][legajo]
            print(f"Empleado: {empleado['nombre']}")
            break
        else:
            print("Legajo no encontrado")
    # verificar dias disponibles
    dias_disponibles = empleado["dias_disponibles"]
    if dias_disponibles <= 0:
        print("Bot: No tienes dias disponibles")
        print("Bot: Gracias por usar el bot")
        print("="*30)
        return
    print(f"Bot: Tienes {dias_disponibles} dias disponibles")

    # solicitar fecha de inicio
    fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/yyyy): ")
    while not validar_fecha(fecha_inicio):
        print("Bot: Fecha de inicio invalida")
        fecha_inicio = input("Ingrese la fecha de inicio (dd/mm/yyyy): ")
    # solicitar fecha de fin
    fecha_fin = input("Ingrese la fecha de fin (dd/mm/yyyy): ")
    while not validar_fecha(fecha_fin) or not fecha_fin_valida(fecha_inicio, fecha_fin):
        print("Bot: Fecha de fin invalida")
        fecha_fin = input("Ingrese la fecha de fin (dd/mm/yyyy): ")
        
    # verificar si el pedido cabe en el saldo 
    dias_solicitados = calcular_dias(fecha_inicio, fecha_fin)
    if dias_solicitados > dias_disponibles:
        print(f"Bot: No tienes suficientes dias disponibles para la solicitud. Tienes {dias_disponibles} dias disponibles")
        print("Bot: Gracias por usar el bot")
        print("="*30)
        return
    else:
        print(f"Bot: Tienes {dias_solicitados} dias disponibles para la solicitud")

    # aprobacion automatica
    print("Bot: Solicitud aprobada")

    # RRHH guarda los dias 
    datos["empleados"][legajo]["dias_disponibles"] -= dias_solicitados

    # guardar los datos
    solicitud = {
        "id": "SOL-" + str(len(datos["solicitudes"]) + 1),
        "legajo": legajo,
        "nombre": empleado["nombre"],
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "dias": dias_solicitados,
        "estado": "APROBADA"
    }
    datos["solicitudes"].append(solicitud)
    guardar_datos(datos)
    print("Bot: Gracias por usar el bot")
    print("="*30)
    
    #notificacion final 
    saldo_restante = datos["empleados"][legajo]["dias_disponibles"]
    print("\n" + "="*45)
    print("  RRHH: SOLICITUD APROBADA")
    print("="*45)
    print(f"  ID:             {solicitud['id']}")
    print(f"  Empleado:       {empleado['nombre']}")
    print(f"  Desde:          {fecha_inicio}")
    print(f"  Hasta:          {fecha_fin}")
    print(f"  Dias tomados:   {dias_solicitados}")
    print(f"  Saldo restante: {saldo_restante} dias")
    print("="*45)
    print("  Que disfrutes tus vacaciones! 🌴")
    print("="*45 + "\n")