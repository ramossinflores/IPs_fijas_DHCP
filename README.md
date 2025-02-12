# 🚀 Script de Configuración de IPs Fijas en DHCP

## 📌 Descripción

Este repo contiene un script en Python que permite configurar direcciones IP fijas en dispositivos a partir de un archivo de texto. El script lee la información de los dispositivos (nombre, dirección MAC y ámbito) y genera las entradas necesarias en el fichero de configuración del servicio ISC DHCP.

Este proyecto es parte de la asignatura **Servicios de Redes e Internet** del ciclo formativo de **Administración de Sistemas Informáticos en Red (ASIR)**. Se trata de una **primera versión** del script, que será mejorada en futuras iteraciones para optimizar su rendimiento y seguridad.

## ⚙️ Funcionamiento

El script realiza las siguientes tareas:

1. ✅ Comprueba que el número de argumentos suministrados es válido.
2. 📄 Lee el fichero CSV proporcionado como argumento.
3. 🔍 Extrae y muestra los siguientes datos por cada línea:
   - 🖥️ Nombre del dispositivo.
   - 🔗 Dirección MAC.
   - 🌐 Ámbito de red.
4. 📌 Asigna una dirección IP fija a cada dispositivo según su ámbito:
   - **🖥️ Server** → Rango 10.206.71.X
   - **💻 Desktop** → Rango 10.206.72.X
   - **📡 Wireless** → Rango 10.206.73.X
5. 🔎 Verifica que la IP generada no esté ya asignada.
6. 📝 Escribe la configuración en el archivo de configuración DHCP.
7. 📡 Realiza pruebas de conectividad mediante `ping` a las nuevas IPs asignadas.

## 📋 Adicional

- 📄 Se incluye un fichero de prueba llamado `IP_Fijas.txt` para verificar la funcionalidad del script.
- 📓 También notas en un Jupyter Notebook con las bases vistas en clase antes de desarrollar el script.

## 📌 Mejoras Futuras

- 🔍 Implementar validación avanzada del formato del archivo CSV.
- ⚠️ Añadir manejo de errores más robusto en la asignación de IPs.
- ⏳ Optimizar la verificación de direcciones IP ya asignadas.
- 🌍 Integrar soporte para más ámbitos de red.
- 🛠️ Reestructurar el código para reducir repeticiones y mejorar su modularidad mediante funciones adicionales.

## 👨‍💻 Autor

 Actualmente, estoy aprendiendo Python, por lo que cualquier sugerencia, mejora o crítica constructiva será **bienvenida**.
Se encuentra en constante mejora. Se aceptan sugerencias y criticas 💡🚀
