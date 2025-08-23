#!/usr/bin/env python3
import os
import subprocess
import zipfile

# --- Configuración ---
BACKEND_DIR = os.path.expanduser("~/english-course-pwa-backend")
FRONTEND_DIR = os.path.expanduser("~/english-course-pwa-frontend")  # cambia si es otro
GITHUB_URL = "https://github.com/Cristobal2929/english-course-pwa-backend.git"
RENDER_URL = "https://english-course-pwa-backend.onrender.com/"
NEFRYTI_UPLOAD_PATH = os.path.expanduser("~/english-course-pwa-frontend.zip")  # temp zip

# --- Paso 1: Backend ---
print("🚀 Actualizando backend...")
bot_file = None
for file in os.listdir(BACKEND_DIR):
    if file.endswith(".py"):
        with open(os.path.join(BACKEND_DIR, file), "r") as f:
            if "Flask" in f.read():
                bot_file = os.path.join(BACKEND_DIR, file)
                break
if not bot_file:
    print("❌ No se encontró ningún archivo .py con Flask en backend")
    exit(1)

with open(bot_file, "r") as f:
    lines = f.readlines()

# Insertar CORS
if not any("from flask_cors import CORS" in line for line in lines):
    lines.insert(0, "from flask_cors import CORS\n")
if not any("CORS(app)" in line for line in lines):
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if "app = Flask" in line:
            new_lines.append("CORS(app)\n")
    lines = new_lines

# Ruta raíz
if not any("@app.route('/')" in line for line in lines):
    lines.append("\n@app.route('/')\ndef index():\n    return 'Backend activo ✅'\n")

with open(bot_file, "w") as f:
    f.writelines(lines)

# Commit y push backend
os.chdir(BACKEND_DIR)
subprocess.run(["git", "add", "."])
commit = subprocess.run(["git", "commit", "-m", "Actualización automática fullstack"], capture_output=True, text=True)
if "nothing to commit" not in commit.stdout:
    subprocess.run(["git", "push", "origin", "main"])
    print("✅ Backend subido a GitHub")
else:
    print("✅ Backend ya estaba actualizado")

# --- Paso 2: Actualizar fetch() en frontend ---
print("🚀 Actualizando fetch() en frontend...")
for root, dirs, files in os.walk(FRONTEND_DIR):
    for file in files:
        if file.endswith(".js"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            content = content.replace("http://localhost:5000", RENDER_URL)
            with open(path, "w") as f:
                f.write(content)

# --- Paso 3: Comprimir frontend y subir a Nefryti ---
print("🚀 Comprimiendo frontend...")
with zipfile.ZipFile(NEFRYTI_UPLOAD_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(FRONTEND_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, FRONTEND_DIR)
            zipf.write(file_path, arcname)
print(f"✅ Frontend comprimido en {NEFRYTI_UPLOAD_PATH}")
print("💡 Sube este zip a Nefryti manualmente o con tu script de Nefryti")

# --- Paso 4: URLs finales ---
print("\n🌐 Backend Render:", RENDER_URL)
print("🌐 Frontend Nefryti: [sube tu zip manualmente]")

