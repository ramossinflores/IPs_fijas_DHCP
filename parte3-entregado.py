import sys
import os 
from datetime import datetime
import subprocess

# Inicia el script 
start_time = (datetime.now()).strftime("%H:%M:%S.%f")[:-3]

# Verificando el número de argumentos:
if len(sys.argv) != 2: # Contando el nombre del script
    print("ERROR. Debe introducir solo un argumento: fichero.csv")
    sys.exit(1) #Salida con errores

# Se extrae el fichero de los argumentos
file = sys.argv[1]

# Inicio en 5 para no machacar los dispositivos estáticos que ya tengo en mi configuración
server_hosts_ip_count = 5
desktop_hosts_ip_count =5 
wireless_hosts_ip_count = 5    

# Función para revisar que el dispositivo por agregar no esté registrado antes
def ip_exists(ip):
    # Lee el archivo dhcp.conf
    with open('prueba.txt', 'r') as dhcp_conf:
        # Recorre cada línea del archivo de configuración
        for line in dhcp_conf:
            if f"fixed-address {ip}" in line:# Si la línea contiene la IP buscada ... 
                return True  # Devuelve true si la IP ya está asignada
    return False  # Y falso si la IP no está asignada


# Función para imprimir con  el formato de host estático en el dhcp.conf
def host_configuration(file_handle,device_name, mac, fixed_ip):
    configuration = (
        "\thost " + device_name + " {\n"
        + "\t\thardware ethernet " + mac + ";\n"
        + "\t\tfixed-address " + fixed_ip + ";\n"
        + "\t}\n"
    )
    file_handle.write(configuration)



# Confirmando la existencia dle fichero 
# 🖊️  https://www.geeksforgeeks.org/python-os-path-isfile-method/
if not os.path.isfile(file):
    print(f"No se encontró el fichero: {file} \n Verifique el nombre.")
    sys.exit(1) #Salida con errores

# Inicializo las listas vacías donde se guardarán los dispositivos en cada ámbito
server_devices=[]
desktop_devices=[]
wireless_devices=[]

# Leer el archivo
with open(file, 'r') as  file:
    lines = file.readlines()
    for line in lines[1:]: # Para cada línea en el archivo dado como argumento, excepto la primera línea que es encabezado
        fields = line.strip().split(';') 
        """ 
        strip() Remove spaces at the beginning and at the end of the string 
        ->>  string.strip(characters)
        slipt() Split a string into a list where each word is a list item 
        ->> string.split(separator, maxsplit)
        """ 
        if len(fields) != 3: # número de ítems en la matriz fields, es diferente de 3??!
            print(f"La línea {line} no tiene los campos esperados.")  ##ERROR
            continue
        # Asigno las variables a cada campo de la lista
        device_name, mac, scope = fields
        """
        # Imprimiendo los datos por cada línea
        print (f"Nombre del dispositivo: '{device_name} \n") 
        print (f"Dirección MAC: '{mac} \n")
        print (f"Ámbito: '{scope} \n") 
        """        
        # Clasificar  los dispositivos según su ámbito

        if scope == "Server":
            if server_hosts_ip_count <= 10:    
                server_subnet="10.206.71"
                while True:
                        fixed_ip = f"{server_subnet}.{server_hosts_ip_count}" # Genero una IP fija concatenando el scope y y el ip_count
                        if not ip_exists(fixed_ip):
                            server_devices.append([device_name, mac, fixed_ip]) # Agrego los elementos que necesito para mi función que imprime los host estáicos
                            server_hosts_ip_count +=1 # Se suma una unidad para la siguiente IP par seguir la secuencia
                            break
                        else:
                            print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                            server_hosts_ip_count += 1  # Incremento  para probar con la siguiente IP
        elif scope == "Desktop":
            if desktop_hosts_ip_count <= 19:       
                desktop_subnet="10.206.72"
                while True: 
                    fixed_ip = f"{desktop_subnet}.{desktop_hosts_ip_count}"
                    if not ip_exists(fixed_ip):
                        desktop_devices.append([device_name, mac, fixed_ip])
                        desktop_hosts_ip_count +=1
                        break
                    else:
                        print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                        desktop_hosts_ip_count +=1                    
        elif scope == "Wireless":
            if wireless_hosts_ip_count <= 29:       
                wireless_subnet="10.206.73"
                while True:    
                    fixed_ip = f"{wireless_subnet}.{wireless_hosts_ip_count}"
                    if not ip_exists(fixed_ip):
                        wireless_devices.append([device_name, mac, fixed_ip])
                        wireless_hosts_ip_count +=1
                        break
                    else:
                        print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                        wireless_hosts_ip_count +=1
        else:
            print(f"Ámbito desconocido {scope} para el dispositivo {device_name}")

# Lista de todos los dispostivos insertados: 
added_devices =  server_devices + desktop_devices + wireless_devices
# Registros insertados
total_inserted=len(added_devices)

'''    Impresión en listas separadas  
print("="*50+"\n\tServidores"+"\n"+"="*50+"\n")
for server in server_devices:
    host_configuration(server[0], server[1], server[2])
print("="*50+"\n\tDesktops"+"\n"+"="*50+"\n")
for desktop in desktop_devices:
    host_configuration(desktop[0], desktop[1], desktop[2])
print("="*50+"\n\tWireless"+"\n"+"="*50+"\n")
for wireless in wireless_devices:
    host_configuration(wireless[0], wireless[1], wireless[2])    
'''
# Añadir al fichero de configuración
""" open('prueba.txt', 'a') as dhcp_conf: 
    para abrir el archivo  de configuración dhcp y añadir los  dispositivos 
    con IP estática"""
with open("prueba.txt", "a") as dhcp_conf: 
    dhcp_conf.write("group Servidores{\n")
    for server in server_devices:
        host_configuration(dhcp_conf,server[0], server[1], server[2])
    dhcp_conf.write("}\ngroup Desktops{\n")
    for desktop in desktop_devices:
        host_configuration(dhcp_conf,desktop[0], desktop[1], desktop[2])
    dhcp_conf.write("}\ngroup Wireless{\n")
    for wireless in wireless_devices:
        host_configuration(dhcp_conf,wireless[0], wireless[1], wireless[2])    
    dhcp_conf.write("}") 


print("\nRealizando prueba de conectividad para dispositivos nuevos...")
active_devices = 0
for device in added_devices:
# subprocess.run permite ejecutar comandos del sistema 
    response = subprocess.run(["ping", "-c", "1", device[2]], stdout=subprocess.PIPE)  # "-c", "1": que solo envíe 1 paquete
    #  stdout=subprocess.PIPE redirige la salida estándar (resultado exitoso) 
    # y stderr=subprocess.PIPE captura la salida de error si algo falla.
    if response.returncode == 0: # si es 0 significa que el comando fue exitoso
        print(f"{device[2]} está activa.")
        print("Resultado de ping:", response.stdout.decode()) # .stout salida estándar del comando, .decode pasa esos bytes a str
        active_devices += 1 # un dispositivo activo
    else: # si es distinto de 0 significa que el comando falló
            print(f"No se pudo contactar a {device[2]}")

# Final del script 
end_time = (datetime.now()).strftime("%H:%M:%S")
# Impresión del log 
print("\n="*50+"\nLOG"+"\n"+"="*50+"\n")
print(f"Hora de inicio: {start_time}")
print(f"Registros totales insertados: {total_inserted}")
print(f"Dispositivos activos tras asignación de IP: {active_devices}")
print(f"Hora de finalización: {end_time}")

