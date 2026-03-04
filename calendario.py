import calendar
import datetime
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

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

    festivos = {
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

    return festivos

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

hablar("Bienvenido al calendario accesible auditivo")
print("Bienvenido al calendario accesible auditivo")

while True:
    print("\nSeleccione una opción:")
    print("1. Ver calendario de un mes")
    print("2. Calcular qué día cae una fecha y cuántos días faltan")
    print("3. Salir")

    hablar("Seleccione una opción. Uno para ver el calendario mensual, dos para calcular el día de una fecha, o tres para salir.")

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        try:
            numero_mes = int(input("Ingrese número del mes (1-12): "))
            año = int(input("Ingrese el año: "))

            if 1 <= numero_mes <= 12:

                nombre_mes = meses[numero_mes - 1]
                festivos = obtener_festivos(año)

                print(f"\n📅 Calendario de {nombre_mes} {año}:\n")
                hablar(f"Calendario de {nombre_mes} del año {año}")

                cal = calendar.TextCalendar(firstweekday=0)
                calendario_str = cal.formatmonth(año, numero_mes)

                for eng, esp in zip(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], dias_semana):
                    calendario_str = calendario_str.replace(eng, esp[:2])

                print(calendario_str)

                primer_dia, total_dias = calendar.monthrange(año, numero_mes)

                print("🎉 Días festivos del mes:\n")
                for dia in range(1, total_dias + 1):
                    if (dia, numero_mes) in festivos:
                        nombre = festivos[(dia, numero_mes)]
                        print(f"📌 {dia} de {nombre_mes}: {nombre}")
                        hablar(f"El {dia} de {nombre_mes} es {nombre}")

                dia_inicio = dias_semana[primer_dia]
                hablar(f"El mes de {nombre_mes} empieza en {dia_inicio} y tiene {total_dias} días.")

            else:
                print("❌ Número de mes no válido")
                hablar("Número de mes no válido")

        except ValueError:
            print("❌ Entrada inválida.")
            hablar("Entrada inválida.")

    elif opcion == "2":
        fecha_str = input("Ingrese una fecha (dd/mm/aaaa): ")
        try:
            fecha_obj = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            hoy = datetime.date.today()

            festivos = obtener_festivos(fecha_obj.year)

            nombre_dia = dias_semana[fecha_obj.weekday()]
            dias_restantes = (fecha_obj - hoy).days

            print(f"\n📅 La fecha {fecha_str} cae en {nombre_dia}.")
            hablar(f"Esa fecha cae en {nombre_dia}")

            clave = (fecha_obj.day, fecha_obj.month)
            if clave in festivos:
                festivo = festivos[clave]
                print(f"🎉 Es un día festivo: {festivo}")
                hablar(f"Es un día festivo: {festivo}")

            if dias_restantes > 0:
                print(f"⏳ Faltan {dias_restantes} días para esa fecha.")
                hablar(f"Faltan {dias_restantes} días para esa fecha.")
            elif dias_restantes == 0:
                print("✅ Esa fecha es hoy.")
                hablar("Esa fecha es hoy.")
            else:
                print(f"📅 Esa fecha cayó hace {abs(dias_restantes)} días.")
                hablar(f"Esa fecha cayó hace {abs(dias_restantes)} días.")

        except ValueError:
            print("❌ Formato inválido. Use el formato dd/mm/aaaa.")
            hablar("Formato inválido. Intente de nuevo.")

    elif opcion == "3":
        print("Gracias por usar el calendario accesible.")
        hablar("Gracias por usar el calendario accesible.")
        break

    else:
        print("❌ Opción no válida, intente de nuevo.")
        hablar("Opción no válida, intente de nuevo.")