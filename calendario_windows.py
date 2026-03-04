from calendario_core import *
import datetime

def main():
    print("=== Calendario Inteligente ===")
    print("1. Ver calendario de un mes")
    print("2. Analizar una fecha")
    
    opcion = input("Elige una opción (1 o 2): ")

    if opcion == "1":
        año = int(input("Ingresa el año: "))
        mes = int(input("Ingresa el mes (1-12): "))
        
        datos = obtener_calendario_mes(año, mes)
        
        print("\nMes:", datos["nombre_mes"])
        print(datos["calendario"])
        print("Primer día:", datos["primer_dia"])
        print("Total de días:", datos["total_dias"])

    elif opcion == "2":
        fecha_str = input("Ingresa la fecha (dd/mm/aaaa): ")
        dia, mes, año = map(int, fecha_str.split("/"))
        fecha_obj = datetime.date(año, mes, dia)

        resultado = analizar_fecha(fecha_obj)

        print("Día:", resultado["nombre_dia"])
        
        if resultado["festivo"]:
            print("Es festivo:", resultado["festivo"])

        if resultado["dias_restantes"] > 0:
            print("Faltan", resultado["dias_restantes"], "días.")
        elif resultado["dias_restantes"] == 0:
            print("Esa fecha es hoy.")
        else:
            print("Esa fecha ya pasó hace", abs(resultado["dias_restantes"]), "días.")

    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()