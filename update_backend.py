#!/usr/bin/env python3
import os
import subprocess

BACKEND_DIR = os.path.expanduser("~/english-course-pwa-backend")
GITHUB_URL = "https://github.com/Cristobal2929/english-course-pwa-backend.git"
RENDER_URL = "https://english-course-pwa-backend.onrender.com/"

if not os.path.isdir(BACKEND_DIR):
    print(f"❌ No se encontró la carpeta {BACKEND_DIR}")
    exit(1)

# --- Paso 1: Encontrar el archivo Python que contiene Flask ---
bot_file = None
for file in os.listdir(BACKEND_DIR):
    if file.endswith(".py"):
        with open(os.path.join(BACKEND_DIR, file), "r") as f:
            content = f.read()
            if "Flask" in content:
                bot_file = os.path.join(BACKEND_DIR, file)
                break

if not bot_file:
    print("❌ No se encontró ningún archivo .py con Flask")
    exit(1)

print(f"⚡ Archivo backend encontrado: {bot_file}")

# --- Paso 2: Leer y modificar el archivo ---
with open(bot_file, "r") as f:
    lines = f.readlines()

# Insertar import CORS si no existe
if not any("from flask_cors import CORS" in line for line in lines):
    lines.insert(0, "from flask_cors import CORS\n")
    print("⚡ Import CORS agregado")

# Insertar CORS(app)
cors_added = any("CORS(app)" in line for line in lines)
new_lines = []
for line in lines:
    new_lines.append(line)
    if not cors_added and "app = Flask" in line:
        new_lines.append("CORS(app)\n")
        cors_added = True
        print("⚡ CORS(app) agregado")

# Insertar ruta raíz /
if not any("@app.route('/')" in line for line in new_lines):
    new_lines.append("\n@app.route('/')\ndef index():\n    return 'Backend activo ✅'\n")
    print("⚡ Ruta '/' agregada")

# Guardar cambios
with open(bot_file, "w") as f:
    f.writelines(new_lines)

# --- Paso 3: Commit y push a GitHub ---
os.chdir(BACKEND_DIR)
subprocess.run(["git", "add", "."])
commit = subprocess.run(["git", "commit", "-m", "Actualización automática: CORS + /"], capture_output=True, text=True)

if "nothing to commit" in commit.stdout:
    print("✅ No hay cambios nuevos para commit")
else:
    print("⚡ Commit creado")
    subprocess.run(["git", "push", "origin", "main"])
    print("🚀 Cambios subidos a GitHub")

# --- Paso 4: Mostrar URL de Render ---
print(f"🌐 Verifica tu backend en Render: {RENDER_URL}")

