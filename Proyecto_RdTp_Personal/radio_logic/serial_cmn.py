import serial, time

def conectaresp():
    try:
        #Intenta establecer comunicación con esp32 sin cerrar puerto
        esp=serial.Serial("COM4",9600)
        esp.setDTR(True)
        esp.setRTS(True)
        return esp
    except: #En caso de algún error inesperado
        print("No hay un dispositivo conectado, por favor revise su puerto...")
        return None

def sendAzAlt(esp,az, alt):
    coords = f"{az:.2f},{alt:.2f}\n" #Prepera las coordenadas para ser procesadas y separadas en esp32
    try:
        esp.write(coords.encode('utf-8')) #Envia coordenadas
        time.sleep(0.1)
    except:
        print("Error al enviar datos..")