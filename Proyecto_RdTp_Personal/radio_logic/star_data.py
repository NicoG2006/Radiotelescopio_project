import json
from radio_logic import astronomy_logic as astro

#name of file json
file = "data.json"

#function for save some data in file
def guardar_obj(name: str, ra:float, dec:float):
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    #Create dicctionary for name -> ra, dec
    data[name] = {"ra": ra, "dec": dec}

    #Save in file
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

    return True

#Function for track any object saved
def buscar_obj(name: str):
    #Carga dato en variable
    try:
        with open("data.json", "r") as f:
            data = json.load(f)

        if name in data:
            ra = data[name]["ra"]
            dec = data[name]["dec"]
            return ra,dec
        return None
            
    except FileNotFoundError:
        return None
