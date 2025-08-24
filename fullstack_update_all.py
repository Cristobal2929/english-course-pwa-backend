#!/usr/bin/env python3
import os
import re
import subprocess
from datetime import datetime

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
FRONTEND_DIR = os.path.expanduser("~/english-course-pwa-frontend")
BACKEND_DIR = os.path.expanduser("~/english-course-pwa-backend")
FRONTEND_ZIP = os.path.join(FRONTEND_DIR, f"frontend_nefryti_{int(datetime.now().timestamp())}.zip")
BACKEND_REPO = "https://github.com/Cristobal2929/english-course-pwa-backend.git"
FRONTEND_REPO = "https://github.com/Cristobal2929/english-course-pwa-frontend.git"
BACKEND_URL = "https://english-course-pwa-backend.onrender.com"

# -----------------------------
# FUNCIONES
# -----------------------------
def update_fetch_urls():
    print("🚀 Actualizando fetch() en frontend...")
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            if file.endswith(".js"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                new_content = re.sub(r'fetch\(["\']https?://[^\s"\']+', f'fetch("{BACKEND_URL}', content)
                with open(path, "w") as f:
                    f.write(new_content)
                print(f"✅ Actualizado {path}")
    print("🎉 Todas las llamadas fetch() apuntan al backend de Render")

def git_commit_and_push(repo_dir, message):
    os.chdir(repo_dir)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push", "origin", "main"])
    print(f"🚀 Cambios subidos a GitHub desde {repo_dir}")

def zip_frontend():
    os.chdir(FRONTEND_DIR)
    subprocess.run(["zip", "-r", FRONTEND_ZIP, "*"])
    print(f"📦 Frontend comprimido listo: {FRONTEND_ZIP}")

# -----------------------------
# EJECUCIÓN
# -----------------------------
print("🌐 Iniciando actualización fullstack...")

# 1️⃣ Actualizar fetch() en frontend
update_fetch_urls()

# 2️⃣ Subir cambios al backend y frontend
git_commit_and_push(BACKEND_DIR, f"Update backend URL {BACKEND_URL}")
git_commit_and_push(FRONTEND_DIR, f"Update fetch() URLs to {BACKEND_URL}")

# 3️⃣ Comprimir frontend para Nefryti
zip_frontend()

print("🎉 Fullstack actualizado y listo para desplegar!")

