
import calendar
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import pyttsx3


calendar.setfirstweekday(calendar.MONDAY)

RUTA_BASE = Path(__file__).resolve().parent
ARCHIVO_BD = RUTA_BASE / "calendario.db"

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


def conectar_bd():
    return sqlite3.connect(ARCHIVO_BD)


def inicializar_bd():
    with conectar_bd() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL UNIQUE,
                descripcion TEXT NOT NULL
            )
            """
        )


def hablar(texto):
    print(texto)
    engine.say(texto)
    engine.runAndWait()


def agregar_evento(fecha, descripcion):
    try:
        with conectar_bd() as conexion:
            conexion.execute(
                """
                INSERT INTO eventos (fecha, descripcion)
                VALUES (?, ?)
                """,
                (fecha, descripcion)
            )

        return True

    except sqlite3.IntegrityError:
        return False


def obtener_evento(fecha):
    with conectar_bd() as conexion:
        resultado = conexion.execute(
            """
            SELECT descripcion
            FROM eventos
            WHERE fecha = ?
            """,
            (fecha,)
        ).fetchone()

    if resultado:
        return resultado[0]

    return None


def listar_eventos():
    with conectar_bd() as conexion:
        resultados = conexion.execute(
            """
            SELECT fecha, descripcion
            FROM eventos
            ORDER BY fecha
            """
        ).fetchall()

    return resultados


def eliminar_evento(fecha):
    with conectar_bd() as conexion:
        cursor = conexion.execute(
            """
            DELETE FROM eventos
            WHERE fecha = ?
            """,
            (fecha,)
        )

        return cursor.rowcount > 0


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

        date(anio, 3, 8):
        "Día de la mujer",

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

        date(anio, 12, 31):
        "Año viejo",

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


def ver_dia(anio, mes, dia):

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

    evento = obtener_evento(clave)

    if evento:

        hablar(
            "Evento: "
            + evento
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


def convertir_fecha(texto):

    texto = texto.strip()

    try:

        return datetime.strptime(
            texto,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return datetime.strptime(
            texto,
            "%d/%m/%Y"
        ).date()


def agregar_evento_desde_consola():

    try:

        texto = input(
            "Fecha (AAAA-MM-DD o DD/MM/AAAA): "
        ).strip()

        fecha = convertir_fecha(
            texto
        )

        descripcion = input(
            "Descripción: "
        ).strip()

        if not descripcion:

            hablar(
                "La descripción no puede estar vacía"
            )

            return

        guardado = agregar_evento(
            fecha.isoformat(),
            descripcion
        )

        if guardado:

            hablar(
                "Evento guardado correctamente"
            )

        else:

            hablar(
                "Ya existe un evento en esa fecha"
            )

    except ValueError:

        hablar(
            "Formato de fecha inválido. "
            "Use AAAA-MM-DD o DD/MM/AAAA"
        )


def mostrar_eventos():

    eventos = listar_eventos()

    if not eventos:

        hablar(
            "No hay eventos guardados"
        )

        return

    print()

    for fecha, descripcion in eventos:

        print(
            fecha,
            "-",
            descripcion
        )


def eliminar_evento_desde_consola():

    try:

        texto = input(
            "Ingrese fecha del evento "
            "(AAAA-MM-DD o DD/MM/AAAA): "
        ).strip()

        fecha = convertir_fecha(
            texto
        )

        eliminado = eliminar_evento(
            fecha.isoformat()
        )

        if eliminado:

            hablar(
                "Evento eliminado"
            )

        else:

            hablar(
                "No existe un evento en esa fecha"
            )

    except ValueError:

        hablar(
            "Formato de fecha inválido. "
            "Use AAAA-MM-DD o DD/MM/AAAA"
        )


if __name__ == "__main__":

    inicializar_bd()

    print(
        "Base de datos inicializada correctamente."
    )
