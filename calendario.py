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

DIAS_LARGOS = [
    "Lunes", "Martes", "Miércoles",
    "Jueves", "Viernes", "Sábado", "Domingo"
]


def hablar(texto):
    print(texto)
    engine.say(texto)
    engine.runAndWait()


def cargar_eventos():

    if os.path.exists(ARCHIVO_EVENTOS):

        try:

            with open(
                ARCHIVO_EVENTOS,
                "r",
                encoding="utf-8"
            ) as archivo:

                return json.load(archivo)

        except json.JSONDecodeError:

            hablar(
                "El archivo de eventos está dañado"
            )

            return {}

        except Exception:

            hablar(
                "No se pudieron cargar los eventos"
            )

            return {}

    return {}


def guardar_eventos(eventos):

    try:

        with open(
            ARCHIVO_EVENTOS,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                eventos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    except Exception:

        hablar(
            "No se pudieron guardar los eventos"
        )


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

    dia = (
        (h + l - 7 * m + 114) % 31
    ) + 1

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

    return segundo_domingo(
        anio,
        mes
    ) + timedelta(days=7)


def festivos_colombia(anio):

    pascua = calcular_pascua(anio)

    festivos = {

        date(anio, 1, 1):
        "Año Nuevo",

        date(anio, 5, 1):
        "Día del Trabajo",

        date(anio, 7, 20):
        "Independencia de Colombia",

        date(anio, 8, 7):
        "Batalla de Boyacá",

        date(anio, 12, 8):
        "Inmaculada Concepción",

        date(anio, 12, 25):
        "Navidad",

        date(anio, 11, 14):
        "Cumpleaños del desarrollador",

        siguiente_lunes(
            date(anio, 1, 6)
        ):
        "Reyes Magos",

        siguiente_lunes(
            date(anio, 3, 19)
        ):
        "San José",

        siguiente_lunes(
            date(anio, 6, 29)
        ):
        "San Pedro y San Pablo",

        siguiente_lunes(
            date(anio, 8, 15)
        ):
        "Asunción de la Virgen",

        siguiente_lunes(
            date(anio, 10, 12)
        ):
        "Día de la Raza",

        siguiente_lunes(
            date(anio, 11, 1)
        ):
        "Todos los Santos",

        siguiente_lunes(
            date(anio, 11, 11)
        ):
        "Independencia de Cartagena",

        pascua - timedelta(days=3):
        "Jueves Santo",

        pascua - timedelta(days=2):
        "Viernes Santo",

        pascua + timedelta(days=43):
        "Ascensión del Señor",

        pascua + timedelta(days=64):
        "Corpus Christi",

        pascua + timedelta(days=71):
        "Sagrado Corazón",

        segundo_domingo(anio, 5):
        "Día de la Madre",

        tercer_domingo(anio, 6):
        "Día del Padre"
    }

    return festivos


def mostrar_mes(anio, mes):

    try:

        festivos = festivos_colombia(anio)

        print()

        print(
            MESES[mes - 1],
            anio
        )

        print(
            " ".join(DIAS)
        )

        semanas = calendar.monthcalendar(
            anio,
            mes
        )

        for semana in semanas:

            fila = []

            for dia in semana:

                if dia == 0:

                    fila.append("   ")

                else:

                    fecha_actual = date(
                        anio,
                        mes,
                        dia
                    )

                    if fecha_actual in festivos:

                        fila.append(
                            (str(dia) + "*").rjust(3)
                        )

                    else:

                        fila.append(
                            str(dia).rjust(3)
                        )

            print(
                " ".join(fila)
            )

        print()

        print(
            "* = Día festivo"
        )

        print()

        hay_festivos = False

        for fecha_festiva, nombre in sorted(
            festivos.items()
        ):

            if fecha_festiva.month == mes:

                hay_festivos = True

                print(
                    fecha_festiva.strftime(
                        "%d/%m/%Y"
                    ),
                    "-",
                    nombre
                )

        if not hay_festivos:

            print(
                "No hay festivos registrados este mes"
            )

    except Exception:

        hablar(
            "No se pudo mostrar el calendario"
        )


def ver_dia(anio, mes, dia, eventos):

    try:

        fecha = date(
            anio,
            mes,
            dia
        )

    except ValueError:

        hablar(
            "Fecha inválida"
        )

        return

    texto_fecha = (

        f"{DIAS_LARGOS[fecha.weekday()]} "

        f"{fecha.day} de "

        f"{MESES[fecha.month - 1]} "

        f"de {fecha.year}"
    )

    hablar(texto_fecha)

    festivos = festivos_colombia(anio)

    if fecha in festivos:

        hablar(
            "Festivo: "
            + festivos[fecha]
        )

    clave = fecha.isoformat()

    if clave in eventos:

        hablar(
            "Evento: "
            + eventos[clave]
        )

    hoy = date.today()

    diferencia = (
        fecha - hoy
    ).days

    if diferencia > 0:

        hablar(
            f"Faltan "
            f"{diferencia} días "
            f"para esta fecha"
        )

    elif diferencia == 0:

        hablar(
            "Esa fecha es hoy"
        )

    else:

        hablar(
            f"Esa fecha ocurrió hace "
            f"{abs(diferencia)} días"
        )


def agregar_evento(eventos):

    try:

        texto = input(
            "Fecha (AAAA-MM-DD o DD/MM/AAAA): "
        ).strip()

        try:

            fecha = datetime.strptime(
                texto,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            fecha = datetime.strptime(
                texto,
                "%d/%m/%Y"
            ).date()

        descripcion = input(
            "Descripción: "
        ).strip()

        if not descripcion:

            hablar(
                "La descripción no puede estar vacía"
            )

            return

        eventos[
            fecha.isoformat()
        ] = descripcion

        guardar_eventos(eventos)

        hablar(
            "Evento guardado correctamente"
        )

    except ValueError:

        hablar(
            "Formato inválido. "
            "Use AAAA-MM-DD "
            "o DD/MM/AAAA"
        )


def eliminar_evento(eventos):

    clave = input(
        "Ingrese fecha del evento "
        "AAAA-MM-DD: "
    ).strip()

    if clave in eventos:

        del eventos[clave]

        guardar_eventos(eventos)

        hablar(
            "Evento eliminado"
        )

    else:

        hablar(
            "No existe un evento "
            "en esa fecha"
        )


def listar_eventos(eventos):

    if not eventos:

        hablar(
            "No hay eventos guardados"
        )

        return

    print()

    for clave in sorted(eventos):

        print(
            clave,
            "-",
            eventos[clave]
        )


def mostrar_hoy(eventos):

    hoy = date.today()

    print()

    print(
        "Fecha actual:",
        hoy.strftime("%d/%m/%Y")
    )

    ver_dia(
        hoy.year,
        hoy.month,
        hoy.day,
        eventos
    )


def menu():

    eventos = cargar_eventos()

    hablar(
        "Bienvenido al calendario "
        "accesible auditivo"
    )

    while True:

        print()

        print(
            "1. Ver mes"
        )

        print(
            "2. Consultar día"
        )

        print(
            "3. Agregar evento"
        )

        print(
            "4. Listar eventos"
        )

        print(
            "5. Mostrar fecha actual"
        )

        print(
            "6. Eliminar evento"
        )

        print(
            "7. Salir"
        )

        opcion = input(
            "Opción: "
        ).strip()

        if opcion == "1":

            try:

                anio = int(
                    input("Año: ")
                )

                mes = int(
                    input(
                        "Mes (1-12): "
                    )
                )

                if 1 <= mes <= 12:

                    mostrar_mes(
                        anio,
                        mes
                    )

                else:

                    hablar(
                        "Mes inválido"
                    )

            except ValueError:

                hablar(
                    "Debe ingresar "
                    "números válidos"
                )

        elif opcion == "2":

            try:

                anio = int(
                    input("Año: ")
                )

                mes = int(
                    input("Mes: ")
                )

                dia = int(
                    input("Día: ")
                )

                ver_dia(
                    anio,
                    mes,
                    dia,
                    eventos
                )

            except ValueError:

                hablar(
                    "Debe ingresar "
                    "números válidos"
                )

        elif opcion == "3":

            agregar_evento(
                eventos
            )

        elif opcion == "4":

            listar_eventos(
                eventos
            )

        elif opcion == "5":

            mostrar_hoy(
                eventos
            )

        elif opcion == "6":

            eliminar_evento(
                eventos
            )

        elif opcion == "7":

            hablar(
                "Hasta luego"
            )

            engine.stop()

            break

        else:

            hablar(
                "Opción inválida"
            )


if __name__ == "__main__":

    menu()
