#!/usr/bin/env python3
import os
import subprocess

# --- Configuración ---
FRONTEND_DIR = os.path.expanduser("~/english-course-pwa-frontend")  # ruta de tu frontend
OLD_URLS = ["http://localhost:5000", "https://english-course-pwa-backend.onrender.com"]  # URLs a reemplazar
NEW_URL = "https://english-course-pwa-backend.onrender.com"

# --- Paso 1: Reemplazar URLs ---
print("🚀 Actualizando URLs del backend en frontend...")
files_modified = 0
for root, dirs, files in os.walk(FRONTEND_DIR):
    for file in files:
        if file.endswith(".js") or file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            new_content = content
            for old in OLD_URLS:
                new_content = new_content.replace(old, NEW_URL)
            if new_content != content:
                with open(path, "w") as f:
                    f.write(new_content)
                files_modified += 1
                print(f"⚡ Actualizado: {path}")

print(f"✅ Total archivos modificados: {files_modified}")

# --- Paso 2: Commit y push a GitHub ---
os.chdir(FRONTEND_DIR)
subprocess.run(["git", "add", "."])
commit = subprocess.run(["git", "commit", "-m", "Actualizar URL del backend a Render"], capture_output=True, text=True)

if "nothing to commit" in commit.stdout:
    print("✅ No hay cambios nuevos para commit")
else:
    subprocess.run(["git", "push", "origin", "main"])
    print("🚀 Cambios subidos a GitHub")

# --- Final ---
print(f"🌐 Ahora todos los fetch() apuntan a: {NEW_URL}")

