import socket

def conectaresp():
    try:
        #Intenta establecer comunicación con esp32 mediante un socket
        #Create a socket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("192.168.4.1",8080)) 
        print("Conexión establecida")    
        return s
    
    except: #En caso de algún error inesperado
        print("No se pudo establecer conexión, revise su red...")
        return None

def sendAzAlt(esp: socket.socket,az, alt):
    coords = f"{az:.2f},{alt:.2f}\n" #Prepera las coordenadas para ser procesadas y separadas en esp32
    try:
        esp.sendall(coords.encode('utf-8')) #Envia coordenadas
    except Exception as e:
        print(f"Error al enviar datos: {e}")
