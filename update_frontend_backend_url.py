#!/usr/bin/env python3
import os
import subprocess

FRONTEND_DIR = os.path.expanduser("~/english-course-pwa-frontend")
NEW_URL = "https://english-course-pwa-backend.onrender.com"

# Lista de patrones antiguos que reemplazar
OLD_URL_PATTERNS = [
    "http://localhost:5000",
    "https://english-course-pwa-backend.onrender.com"  # cualquier URL vieja
]

files_modified = 0

print("🚀 Buscando y reemplazando URLs en frontend...")

for root, dirs, files in os.walk(FRONTEND_DIR):
    for file in files:
        if file.endswith(".js") or file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            new_content = content
            for old_url in OLD_URL_PATTERNS:
                new_content = new_content.replace(old_url, NEW_URL)
            if new_content != content:
                with open(path, "w") as f:
                    f.write(new_content)
                files_modified += 1
                print(f"⚡ Actualizado: {path}")

print(f"✅ Archivos modificados: {files_modified}")

# --- Commit y push ---
os.chdir(FRONTEND_DIR)
subprocess.run(["git", "add", "."])
commit = subprocess.run(
    ["git", "commit", "-m", "Actualizar URL backend a Render"],
    capture_output=True,
    text=True
)

if "nothing to commit" in commit.stdout:
    print("✅ No hay cambios nuevos para commit")
else:
    subprocess.run(["git", "push", "origin", "main"])
    print("🚀 Cambios subidos a GitHub")

print(f"🌐 Todos los fetch() ahora apuntan a: {NEW_URL}")

