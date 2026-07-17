from radio_logic import astronomy_logic as astro
from radio_logic import star_data as sd
import time

def menu(): #Crea menu interactivo de consola
    while True:
        print("="*30)
        print("Bienvenido al sistema de rastreo....")
        print("1. Rastrear nuevo objeto")
        print("2. Rastrear sol")
        print("3. Guardar objeto")
        print("4. Buscar objeto guardado ")
        print("5. Salir ")

        option = input("Ingrese opción: ")
        if option == "1":
            astro.rastrear()
        elif option=="2":
            astro.buscar_sol()
        elif option=="3":
            sd.guardar_obj()
        elif option =="4":
            sd.buscar_obj()
        elif option == "5":
            print("Gracias por usar el sistema...")
            time.sleep(2)
            break
        else:
            print("Opción no valida")

if __name__ == "__main__":
    menu()