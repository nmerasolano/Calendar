import calendar
import json
import os
from datetime import date, datetime, timedelta
import pyttsx3

ARCHIVO_EVENTOS = "eventos_calendario.json"

engine = pyttsx3.init()
engine.setProperty("rate", 180)

MESES = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

DIAS = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]


def hablar(texto):
    print(texto)
    engine.say(texto)
    engine.runAndWait()


def cargar_eventos():
    if os.path.exists(ARCHIVO_EVENTOS):
        with open(ARCHIVO_EVENTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return {}


def guardar_eventos(eventos):
    with open(ARCHIVO_EVENTOS, "w", encoding="utf-8") as archivo:
        json.dump(eventos, archivo, ensure_ascii=False, indent=4)


def calcular_pascua(anio):
    a = anio % 19
    b = anio // 100
    c = anio % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(anio, mes, dia)


def siguiente_lunes(fecha):
    while fecha.weekday() != 0:
        fecha += timedelta(days=1)
    return fecha


def segundo_domingo(anio, mes):
    d = date(anio, mes, 1)
    while d.weekday() != 6:
        d += timedelta(days=1)
    return d + timedelta(days=7)


def tercer_domingo(anio, mes):
    return segundo_domingo(anio, mes) + timedelta(days=7)


def festivos_colombia(anio):
    pascua = calcular_pascua(anio)

    festivos = {
        date(anio, 1, 1): "Año Nuevo",
        date(anio, 5, 1): "Día del Trabajo",
        date(anio, 7, 20): "Independencia de Colombia",
        date(anio, 8, 7): "Batalla de Boyacá",
        date(anio, 12, 8): "Inmaculada Concepción",
        date(anio, 12, 25): "Navidad",

        siguiente_lunes(date(anio, 1, 6)): "Reyes Magos",
        siguiente_lunes(date(anio, 3, 19)): "San José",
        siguiente_lunes(date(anio, 6, 29)): "San Pedro y San Pablo",
        siguiente_lunes(date(anio, 8, 15)): "Asunción de la Virgen",
        siguiente_lunes(date(anio, 10, 12)): "Día de la Raza",
        siguiente_lunes(date(anio, 11, 1)): "Todos los Santos",
        siguiente_lunes(date(anio, 11, 11)): "Independencia de Cartagena",

        pascua - timedelta(days=3): "Jueves Santo",
        pascua - timedelta(days=2): "Viernes Santo",
        pascua + timedelta(days=43): "Ascensión del Señor",
        pascua + timedelta(days=64): "Corpus Christi",
        pascua + timedelta(days=71): "Sagrado Corazón",

        segundo_domingo(anio, 5): "Día de la Madre",
        tercer_domingo(anio, 6): "Día del Padre"
    }

    return festivos


def mostrar_mes(anio, mes):
    print()
    print(MESES[mes - 1], anio)
    print(" ".join(DIAS))

    semanas = calendar.monthcalendar(anio, mes)

    for semana in semanas:
        fila = []
        for dia in semana:
            if dia == 0:
                fila.append("  ")
            else:
                fila.append(str(dia).rjust(2))
        print(" ".join(fila))


def ver_dia(anio, mes, dia, eventos):
    try:
        fecha = date(anio, mes, dia)
    except ValueError:
        hablar("Fecha inválida")
        return

    hablar(fecha.strftime("%A %d de %B de %Y"))

    festivos = festivos_colombia(anio)

    if fecha in festivos:
        hablar("Festivo: " + festivos[fecha])

    clave = fecha.isoformat()

    if clave in eventos:
        hablar("Evento: " + eventos[clave])


def agregar_evento(eventos):
    try:
        texto = input("Fecha AAAA-MM-DD: ").strip()
        fecha = datetime.strptime(texto, "%Y-%m-%d").date()

        descripcion = input("Descripción: ").strip()

        eventos[fecha.isoformat()] = descripcion
        guardar_eventos(eventos)

        hablar("Evento guardado")

    except ValueError:
        hablar("Formato de fecha inválido")


def listar_eventos(eventos):
    if not eventos:
        hablar("No hay eventos guardados")
        return

    for clave in sorted(eventos):
        print(clave, "-", eventos[clave])


def menu():
    eventos = cargar_eventos()

    while True:
        print()
        print("1. Ver mes")
        print("2. Consultar día")
        print("3. Agregar evento")
        print("4. Listar eventos")
        print("5. Hoy")
        print("6. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            anio = int(input("Año: "))
            mes = int(input("Mes (1-12): "))
            mostrar_mes(anio, mes)

        elif opcion == "2":
            anio = int(input("Año: "))
            mes = int(input("Mes: "))
            dia = int(input("Día: "))
            ver_dia(anio, mes, dia, eventos)

        elif opcion == "3":
            agregar_evento(eventos)

        elif opcion == "4":
            listar_eventos(eventos)

        elif opcion == "5":
            hoy = date.today()
            ver_dia(hoy.year, hoy.month, hoy.day, eventos)

        elif opcion == "6":
            engine.stop()
            hablar("Hasta luego")
            break

        else:
            hablar("Opción inválida")


if __name__ == "__main__":
    menu()
