import json
from radio_logic import astronomy_logic as astro

#Función para agregar nuevo objeto celeste en mini base de datos
def guardar_obj():
    #Pedir datos nvo objeto
    print("="*30)
    print("GUARDAR NUEVO OBJETO")
    
    name = astro.object_name()#Pide name
    in_dates = astro.pedir_raDec() #Pide coordenadas
    
    if in_dates is not None: #Evalua que los datos no esten vacion
        ra, dec = in_dates 
        archivo = "data.json" #Nota: NO BORRAR ESTE ARCHIVO NUNCA
        
        # Cargar datos existentes o crear diccionario vacío
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            datos = {}

        # Insertar el nuevo objeto
        datos[name] = {"ra": ra, "dec": dec}

        # Guardar todo el diccionario actualizado
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
            
        print(f"¡{name} guardado con éxito en {archivo}!")
    else:
        print("Error en las coordenadas. No se guardó nada.")

#Función para buscar un objeto existente en la mini base de datos
def buscar_obj():
    #Carga dato en variable
    with open("data.json", "r") as f:
        data = json.load(f)
    name = astro.object_name()
    try:
        #En caso de que si esté...
        if name in data:
            ra = data[name]["ra"]
            dec = data[name]["dec"]
            astro.rastrear(name, ra, dec)
        else: 
            print(f"{name} no existe dentro de la base de datos...")
    except FileNotFoundError: #Si hay un error de archivo inesperado
        print("Porfavor guardar nuevo objeto en base de datos...")
