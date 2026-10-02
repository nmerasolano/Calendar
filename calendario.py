from datetime import date

from funciones_nuevas import (
    inicializar_bd,
    hablar,
    engine,
    mostrar_mes,
    ver_dia,
    agregar_evento_desde_consola,
    mostrar_eventos,
    eliminar_evento_desde_consola
)


def mostrar_hoy():

    hoy = date.today()

    print()

    print(
        "Fecha actual:",
        hoy.strftime("%d/%m/%Y")
    )

    ver_dia(
        hoy.year,
        hoy.month,
        hoy.day
    )


def menu():

    inicializar_bd()

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
                    dia
                )

            except ValueError:

                hablar(
                    "Debe ingresar "
                    "números válidos"
                )

        elif opcion == "3":

            agregar_evento_desde_consola()

        elif opcion == "4":

            mostrar_eventos()

        elif opcion == "5":

            mostrar_hoy()

        elif opcion == "6":

            eliminar_evento_desde_consola()

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
