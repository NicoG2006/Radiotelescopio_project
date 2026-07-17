from astropy.coordinates import AltAz, SkyCoord, EarthLocation, get_sun
from astropy.time import Time
import astropy.units as u
from radio_logic import serial_cmn as sc
import time as t

def pedir_raDec():
    print("="*30)
    print("🛰️ ENTRADA DE COORDENADAS MANUAL")

    indate = input("Ingresar RA y Dec (separados por espacio): ").split()
    print("="*30)
    try:    
        #En caso de que el usuario ingrese más datos
        if len(indate)!=2:
            print("Solo debe registar Alt y Az")
            return None 
    
        #Conviere cada dato en float operable
        coord = SkyCoord(indate[0],indate[1], unit=(u.hourangle, u.deg) if 'h' in indate[0] else (u.deg, u.deg))
        return coord.ra.deg, coord.dec.deg
    except ValueError: #En caso de meter texto o algun caracter no valido
        print("Error, debes ingresar datos en grados y decimales")
        return None
    

def object_name():
    print("="*30)
    indate = input("Ingrese nombre del objeto: ")
    print("="*30)
    return indate
    

def buscar_sol():
    try: #Imprime informaciín previa para el sol
        print("=" * 30)
        print(f"REPORTE SOLAR")
        print(f"Hora UTC: {Time.now()}")
        print("=" * 30)
        esp=sc.conectaresp()
        while True:
            #Cada inicio de bucle debe actualizarce el tiempo por ende se deja acá dentro
            ahora = Time.now()
            sol_pos = get_sun(ahora).transform_to(AltAz(obstime=ahora, location=casa)) #Toma Ra y Dec actual del sol gracias a ahora actualizado
            print("-" * 30)
            print(f"Azimut (Dónde girar): {sol_pos.az:.2f}")
            print(f"Elevación (Cuánto subir): {sol_pos.alt:.2f}")
            print("-" * 30)
            #Envía de inmediato datos de AzAlt en un solo viaje al esp32
            sc.sendAzAlt(esp, sol_pos.az.deg, sol_pos.alt.deg)
            t.sleep(2) #Da espera de 2 segudnos para el próximo calculo      
    except KeyboardInterrupt: #En caso de que desee terminar rastreo hacer Keyinterrupt por ahora..
        print("Ha terminado el rastreo...")

def rastrear(name=None, ra=None, dec=None): #Parametros predeterminados en None
    if (name == None and ra== None and dec==None): #Si no hay entonces preguntar por los datos
        name = object_name() #Pide nombre del objeto
        coords = pedir_raDec() #Pide Ra y Dec

        if coords: #Verifica que si esten bien los datos
            ra, dec = coords
        else:
            return None
    #En caso que los argumentos ya esten (Existen en base de datos)    
    print("=" * 30)
    print(f"REPORTE PARA {name}")
    print(f"Hora UTC: {Time.now()}")
    print("=" * 30)
    try:
        esp=sc.conectaresp()
        while True:
            tempo=Time.now() #actualiza tiempo cada inicio de bucle
            #Calculo de la posición en Ra y dec con respecto al tiempo del objeto ingresado por coordenadas
            objectC = SkyCoord(ra*u.deg,dec*u.deg ) 
            position = objectC.transform_to(AltAz(obstime = Time.now(), location = casa))

            #Imprime en terminal cuanto debe girar en Az y en Alt
            print("-" * 30)        
            print(f"Azimut (Dónde girar): {position.az:.2f}")
            print(f"Elevación (Cuánto subir): {position.alt:.2f}")
            #Establece la comunicación serial de coordenadas en un solo viaje
            sc.sendAzAlt(esp,position.az.deg,position.alt.deg)
            t.sleep(2) #da una espera de 2s
                    
    except KeyboardInterrupt: #Forma de terminar rastreo por ahora
        print("Has terminado el rastreo....")    
        
#constante
casa = EarthLocation(lat=4.51*u.deg, lon = -75.68*u.deg)