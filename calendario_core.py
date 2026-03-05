import calendar
import datetime

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def calcular_pascua(año):
    a = año % 19
    b = año // 100
    c = año % 100
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
    return datetime.date(año, mes, dia)

def obtener_festivos(año):
    pascua = calcular_pascua(año)

    jueves_santo = pascua - datetime.timedelta(days=3)
    viernes_santo = pascua - datetime.timedelta(days=2)
    domingo_ramos = pascua - datetime.timedelta(days=7)
    sabado_santo = pascua - datetime.timedelta(days=1)
    lunes_pascua = pascua + datetime.timedelta(days=1)

    return {
        (1, 1): "Año nuevo",
        (6, 1): "Reyes Magos",
        (8, 3): "Día de la Mujer",
        (19, 3): "San José",

        (domingo_ramos.day, domingo_ramos.month): "Domingo de Ramos",
        (jueves_santo.day, jueves_santo.month): "Jueves Santo",
        (viernes_santo.day, viernes_santo.month): "Viernes Santo",
        (sabado_santo.day, sabado_santo.month): "Sábado Santo",
        (pascua.day, pascua.month): "Domingo de Pascua",
        (lunes_pascua.day, lunes_pascua.month): "Lunes de Pascua",

        (11, 5): "Día de la Madre",
        (15, 5): "Día del Maestro",
        (15, 6): "Día del Padre",

        (20, 7): "Día de la Independencia",
        (15, 8): "Asunción de la Virgen",
        (12, 10): "Día de la Raza",
        (1, 11): "Día de Todos los Santos",
        (3, 11): "Día de los Muertos",

        (14, 11): "Cumpleaños del desarrollador",

        (11, 11): "Independencia de Cartagena",
        (7, 12): "Día de las Velitas",
        (8, 12): "Inmaculada Concepción",
        (24, 12): "Noche Buena",
        (25, 12): "Navidad",
        (31, 12): "Año Viejo"
    }

def obtener_calendario_mes(año, mes):
    cal = calendar.TextCalendar(firstweekday=0)
    calendario_str = cal.formatmonth(año, mes)

    for eng, esp in zip(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], dias_semana):
        calendario_str = calendario_str.replace(eng, esp[:2])

    primer_dia, total_dias = calendar.monthrange(año, mes)

    return {
        "nombre_mes": meses[mes - 1],
        "calendario": calendario_str,
        "primer_dia": dias_semana[primer_dia],
        "total_dias": total_dias
    }

def analizar_fecha(fecha_obj):
    hoy = datetime.date.today()
    nombre_dia = dias_semana[fecha_obj.weekday()]
    dias_restantes = (fecha_obj - hoy).days
    festivos = obtener_festivos(fecha_obj.year)

    clave = (fecha_obj.day, fecha_obj.month)
    es_festivo = festivos.get(clave)

    return {
        "nombre_dia": nombre_dia,
        "dias_restantes": dias_restantes,
        "festivo": es_festivo
    }