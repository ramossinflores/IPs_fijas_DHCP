import sys
import os 
from datetime import datetime
import csv
import subprocess

# Inicia el script 
start_time = (datetime.now()).strftime("%H:%M:%S")

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

# Inicio de las listas de dispostivos
server_devices = []
desktop_devices = []
wireless_devices = []

# Función para revisar que el dispositivo por agregar no esté registrado antes
def ip_exists(ip):
    # Lee el archivo dhcp.conf
    with open(file, 'r') as dhcp_conf:
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

# Leer el archivo con sus encabezados, que serán las keys de un diccionario llamado "rows"
with open(file, "r") as  csv_file:
    rows= csv.DictReader(csv_file,  delimiter=';')
    count_rows=0
    invalid_rows=0
    for row in rows:
        count_rows += 1 # Contador de filas
        if len(row) != 3: # número de ítems en la matriz fields, es diferente de 3??!
            print(f"La fila {count_rows} no tiene los campos esperados.")  ##ERROR
            invalid_rows +=1
            continue
        # Clasificar  los dispositivos según su ámbito
        if row["scope"] == "Server":
            if server_hosts_ip_count <= 10:    # numero de IPs que pueden ser asignadas a los dispositivos
                server_subnet="10.206.71"
                while True:
                        fixed_ip = f"{server_subnet}.{server_hosts_ip_count}" # Genero una IP fija concatenando el scope y y el ip_count
                        if not ip_exists(fixed_ip):
                        # Agrego los elementos que necesito para mi función que imprime los host estáicos
                            server_devices.append({
                                "device_name": row["device_name"],
                                "mac": row["mac"],
                                "fixed_ip": fixed_ip
                            })        
                            server_hosts_ip_count +=1 # Se suma una unidad para la siguiente IP par seguir la secuencia
                            break
                        else:
                            print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                            server_hosts_ip_count += 1  # Incremento  para probar con la siguiente IP
        elif row["scope"] == "Desktop":
            if desktop_hosts_ip_count <= 19:       
                desktop_subnet="10.206.72"
                while True: 
                    fixed_ip = f"{desktop_subnet}.{desktop_hosts_ip_count}"
                    if not ip_exists(fixed_ip):
                        desktop_devices.append({
                            "device_name": row["device_name"],
                            "mac": row["mac"],
                            "fixed_ip": fixed_ip
                        })                        
                        desktop_hosts_ip_count +=1
                        break
                    else:
                        print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                        desktop_hosts_ip_count +=1                    
        elif row["scope"] == "Wireless":
            if wireless_hosts_ip_count <= 29:       
                wireless_subnet="10.206.73"
                while True:    
                    fixed_ip = f"{wireless_subnet}.{wireless_hosts_ip_count}"
                    if not ip_exists(fixed_ip):
                        wireless_devices.append({
                            "device_name": row["device_name"],
                            "mac": row["mac"],
                            "fixed_ip": fixed_ip
                        })
                        wireless_hosts_ip_count +=1
                        break
                    else:
                        print(f"IP {fixed_ip} ya está asignada, probando la siguiente...")
                        wireless_hosts_ip_count +=1
        else:
            print(f"Ámbito desconocido {row["scope"]} para el dispositivo {row["device_name"]}")

        print("Server devices:", server_devices)
        print("Desktop devices:", desktop_devices)
        print("Wireless devices:", wireless_devices)
# Conjunto de todos los dispostivos insertados: 
added_devices = server_devices + desktop_devices + wireless_devices
# Total de registros insertados
total_inserted=len(added_devices)

# Añadir al fichero de configuración
""" open('prueba.txt', 'a') as dhcp_conf: 
    para abrir el archivo  de configuración dhcp y añadir los  dispositivos 
    con IP estática"""
with open("prueba.txt", "a") as dhcp_conf: 
    dhcp_conf.write("group Servidores{\n")
    for server in server_devices:
        host_configuration(dhcp_conf,server["device_name"], server["mac"], server["fixed_ip"])
    dhcp_conf.write("}\ngroup Desktops{\n")
    for desktop in desktop_devices:
        host_configuration(dhcp_conf,desktop["device_name"], desktop["mac"], desktop["fixed_ip"])
    dhcp_conf.write("}\ngroup Wireless{\n")
    for wireless in wireless_devices:
        host_configuration(dhcp_conf, wireless["device_name"], wireless["mac"], wireless["fixed_ip"])   
    dhcp_conf.write("}") 


print("\nRealizando prueba de conectividad para dispositivos nuevos...")
active_devices = 0
# Iterando sobre la lista de diccionarios
for device in added_devices:
# subprocess.run permite ejecutar comandos del sistema 
    response = subprocess.run(["ping", "-c", "1", device["fixed_ip"]], stdout=subprocess.PIPE)  # "-c", "1": que solo envíe 1 paquete
    #  stdout=subprocess.PIPE redirige la salida estándar (resultado exitoso) 
    # y stderr=subprocess.PIPE captura la salida de error si algo falla.
    if response.returncode == 0: # si es 0 significa que el comando fue exitoso
        print(f"{device['device_name']} está activo/a")
        print("Resultado de ping:", response.stdout.decode()) # .stout salida estándar del comando, .decode pasa esos bytes a str
        active_devices += 1 # suma un dispositivo activo
    else: # si es distinto de 0 significa que el comando falló
            print(f"No se pudo contactar a  {device['fixed_ip']} ({device['device_name']})")

# Final del script 
end_time = (datetime.now()).strftime("%H:%M:%S")
# Impresión del log 
print("\n="*50+"\nLOG"+"\n"+"="*50+"\n")
print(f"Hora de inicio: {start_time}")
print(f"Registros totales insertados: {total_inserted}")
print(f"Dispositivos activos tras asignación de IP: {active_devices}")
print(f"Hora de finalización: {end_time}")

