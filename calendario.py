import calendar
import datetime
import pyttsx3

engine = pyttsx3.init()

meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

dias_festivos = {
    (1, 1): "Año nuevo",
    (6, 1): "Reyes Magos",
    (8, 3): "Día de la Mujer",
    (19, 3): "San José",

    # Semana Santa 2025
    (13, 4): "Domingo de Ramos",
    (17, 4): "Jueves Santo",
    (18, 4): "Viernes Santo",
    (19, 4): "Sábado Santo",
    (20, 4): "Domingo de Pascua",
    (21, 4): "Lunes de Pascua",

    (11, 5): "Día de la Madre",
    (15, 5): "Día del Maestro",
    (15, 6): "Día del Padre",

    (20, 7): "Día de la Independencia",
    (15, 8): "Asunción de la Virgen",
    (12, 10): "Día de la Raza",
    (1, 11): "Día de Todos los Santos",
    (3, 11): "Día de los Muertos",

    # FESTIVO PERSONAL
    (14, 11): "Cumpleaños del desarrollador",

    (11, 11): "Independencia de Cartagena",
    (7, 12): "Día de las Velitas",
    (8, 12): "Inmaculada Concepción",
    (24, 12): "Noche Buena",
    (25, 12): "Navidad",
    (31, 12): "Año Viejo"
}
# =============================================================

engine.say("Bienvenido al calendario accesible auditivo")
engine.runAndWait()
print("Bienvenido al calendario accesible auditivo")

while True:
    print("\nSeleccione una opción:")
    print("1. Ver calendario de un mes")
    print("2. Calcular qué día cae una fecha y cuántos días faltan")
    print("3. Salir")

    engine.say("Seleccione una opción. Uno para ver el calendario mensual, dos para calcular el día de una fecha, o tres para salir.")
    engine.runAndWait()

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        try:
            numero_mes = int(input("Ingrese número del mes (1-12): "))
            if 1 <= numero_mes <= 12:
                nombre_mes = meses[numero_mes - 1]
                print(f"\n📅 Calendario de {nombre_mes} 2025:\n")
                engine.say(f"Calendario de {nombre_mes} del año 2025")
                engine.runAndWait()

                cal = calendar.TextCalendar(firstweekday=0)
                calendario_str = cal.formatmonth(2025, numero_mes)

                # Reemplazar encabezados de días al español
                for eng, esp in zip(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], dias_semana):
                    calendario_str = calendario_str.replace(eng, esp[:2])  # abreviado

                print(calendario_str)

                # Listar festivos del mes
                print("🎉 Días festivos del mes:\n")
                for dia in range(1, 32):
                    if (dia, numero_mes) in dias_festivos:
                        nombre = dias_festivos[(dia, numero_mes)]
                        print(f"📌 {dia} de {nombre_mes}: {nombre}")
                        engine.say(f"El {dia} de {nombre_mes} es {nombre}")
                        engine.runAndWait()

                # Info adicional
                primer_dia, total_dias = calendar.monthrange(2025, numero_mes)
                dia_inicio = dias_semana[primer_dia]
                engine.say(f"El mes de {nombre_mes} empieza en {dia_inicio} y tiene {total_dias} días.")
                engine.runAndWait()

            else:
                print("❌ Número de mes no válido")
                engine.say("Número de mes no válido")
                engine.runAndWait()
        except ValueError:
            print("❌ Entrada inválida. Debe ser un número del 1 al 12.")
            engine.say("Entrada inválida. Debe ser un número del 1 al 12.")
            engine.runAndWait()

    elif opcion == "2":
        fecha_str = input("Ingrese una fecha (dd/mm/aaaa): ")
        try:
            fecha_obj = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
            hoy = datetime.date.today()

            nombre_dia = dias_semana[fecha_obj.weekday()]
            dias_restantes = (fecha_obj - hoy).days

            print(f"\n📅 La fecha {fecha_str} cae en {nombre_dia}.")
            engine.say(f"Esa fecha cae en {nombre_dia}")
            engine.runAndWait()

            # Ver si es un festivo
            clave = (fecha_obj.day, fecha_obj.month)
            if clave in dias_festivos:
                festivo = dias_festivos[clave]
                print(f"🎉 Es un día festivo: {festivo}")
                engine.say(f"Es un día festivo: {festivo}")
                engine.runAndWait()

            if dias_restantes > 0:
                print(f"⏳ Faltan {dias_restantes} días para esa fecha.")
                engine.say(f"Faltan {dias_restantes} días para esa fecha.")
            elif dias_restantes == 0:
                print("✅ Esa fecha es hoy.")
                engine.say("Esa fecha es hoy.")
            else:
                print(f"📅 Esa fecha cayó hace {abs(dias_restantes)} días.")
                engine.say(f"Esa fecha cayó hace {abs(dias_restantes)} días.")
            engine.runAndWait()

        except ValueError:
            print("❌ Formato inválido. Use el formato dd/mm/aaaa.")
            engine.say("Formato inválido. Intente de nuevo. Use el formato día, mes y año.")
            engine.runAndWait()

    elif opcion == "3":
        print("Gracias por usar el calendario accesible.")
        engine.say("Gracias por usar el calendario accesible.")
        engine.runAndWait()
        break

    else:
        print("❌ Opción no válida, intente de nuevo.")
        engine.say("Opción no válida, intente de nuevo.")
        engine.runAndWait()
