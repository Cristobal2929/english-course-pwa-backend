#!/bin/bash
# Script universal para unir frontend (Nefryti/Netlify) con backend (Render)
# Funciona aunque lo ejecutes desde cualquier carpeta dentro del proyecto

# --- Detectar ubicación ---
CURRENT_DIR=$(pwd)

# --- Intentar detectar backend y frontend ---
if [ -d "$CURRENT_DIR/english-course-pwa-backend" ]; then
    BACKEND_DIR="$CURRENT_DIR/english-course-pwa-backend"
    FRONTEND_DIR="$CURRENT_DIR/english-course-pwa-frontend"
elif [ -d "$CURRENT_DIR/english-course-pwa-frontend" ] && [ -d "$CURRENT_DIR/../english-course-pwa-backend" ]; then
    FRONTEND_DIR="$CURRENT_DIR/english-course-pwa-frontend"
    BACKEND_DIR="$CURRENT_DIR/../english-course-pwa-backend"
else
    echo "⚠️ No se encontraron las carpetas backend/frontend en la ruta actual."
    echo "Coloca este script en la carpeta padre que contenga ambas carpetas."
    exit 1
fi

# --- URL del backend en Render ---
BACKEND_URL="https://english-course-pwa-backend.onrender.com"

echo "🔧 Configurando Backend en $BACKEND_DIR..."
cd "$BACKEND_DIR" || exit

# --- Asegurar CORS en Flask ---
if [ -f "botm.py" ]; then
    if ! grep -q "CORS(app)" botm.py; then
        echo "⚡ Insertando configuración de CORS en botm.py..."
        sed -i '1i from flask_cors import CORS' botm.py
        sed -i '/app = Flask/a CORS(app)' botm.py
    fi
elif [ -f "ti.py" ]; then
    if ! grep -q "CORS(app)" ti.py; then
        echo "⚡ Insertando configuración de CORS en ti.py..."
        sed -i '1i from flask_cors import CORS' ti.py
        sed -i '/app = Flask/a CORS(app)' ti.py
    fi
else
    echo "⚠️ No se encontró botm.py ni ti.py, revisa tu backend."
fi

# --- Instalar dependencias backend ---
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias backend..."
    pip install -r requirements.txt
else
    echo "⚠️ No se encontró requirements.txt"
fi

echo "✅ Backend listo."

# --- Configurar frontend ---
echo "🔧 Configurando Frontend en $FRONTEND_DIR..."
cd "$FRONTEND_DIR" || exit

# Crear archivo .env
cat > .env <<EOL
# Variables de entorno para frontend
REACT_APP_API_URL=$BACKEND_URL
VITE_API_URL=$BACKEND_URL
NEXT_PUBLIC_API_URL=$BACKEND_URL
EOL

echo "✅ .env creado con la URL del backend"

# --- Instalar dependencias frontend ---
if [ -f "package.json" ]; then
    echo "📦 Instalando dependencias frontend..."
    npm install
    echo "⚡ Compilando frontend..."
    npm run build || npm run build:prod || npm run generate
    echo "👉 Archivos listos en carpeta 'build' o 'dist'"
else
    echo "⚠️ No se encontró package.json, parece que es frontend puro (HTML/JS)."
    echo "👉 Edita tu 'app.js' para usar: $BACKEND_URL"
fi

echo "🎉 Todo listo: frontend configurado con backend en $BACKEND_URL"
