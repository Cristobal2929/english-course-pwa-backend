import fileinput
import sys

# La URL antigua que queremos reemplazar
old_url = "http://127.0.0.1:5000/api"

# La nueva URL de tu backend en Render
new_url = "https://english-course-pwa-backend.onrender.com/api"

# El nombre del archivo que vamos a modificar
file_to_change = "js/app.js"

try:
    print(f"Buscando '{old_url}' en el archivo '{file_to_change}'...")
    with fileinput.FileInput(file_to_change, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(old_url, new_url), end='')
    
    print("✅ ¡El archivo ha sido actualizado exitosamente!")
    print("Se ha creado una copia de seguridad del archivo original con el nombre app.js.bak")

except FileNotFoundError:
    print(f"❌ Error: El archivo '{file_to_change}' no fue encontrado.")
    print("Asegúrate de ejecutar este script desde la carpeta principal del frontend.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")


