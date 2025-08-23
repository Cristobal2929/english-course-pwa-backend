import os
import random
import time
from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from flask_cors import CORS
import jwt

# Inicializar Flask y CORS
app = Flask(__name__)
CORS(app)

# Clave secreta para JWT (JSON Web Token)
app.config['JWT_SECRET_KEY'] = 'mi_super_secreto'

# Cargar usuarios
def cargar_usuarios():
    # En un entorno real, esto se cargaría de una base de datos
    return {'admin': {'password': 'admin'}}

# --- Rutas de la API ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    usuarios = cargar_usuarios()

    if username in usuarios and usuarios[username]['password'] == password:
        # Generar un token JWT
        token = jwt.encode({'username': username, 'exp': time.time() + 3600}, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token.decode('utf-8')})
    else:
        return jsonify({'message': 'Credenciales inválidas'}), 401

@app.route('/api/lecciones', methods=['GET'])
def get_lecciones():
    # Devuelve la lista de lecciones disponibles
    lecciones = [
        {"id": 1, "titulo": "Lección 1: Saludos"},
        {"id": 2, "titulo": "Lección 2: Presentaciones"},
        {"id": 3, "titulo": "Lección 3: Números"},
        # ... agrega más lecciones si lo necesitas
    ]
    return jsonify(lecciones)

@app.route('/api/lecciones/<int:leccion_id>', methods=['GET'])
def get_leccion(leccion_id):
    # Devuelve el contenido de una lección específica
    lecciones_data = {
        1: [
            {"pregunta": "Hello", "respuesta": "Hola"},
            {"pregunta": "Goodbye", "respuesta": "Adiós"}
        ],
        2: [
            {"pregunta": "My name is", "respuesta": "Mi nombre es"},
            {"pregunta": "What is your name?", "respuesta": "¿Cuál es tu nombre?"}
        ],
        3: [
            {"pregunta": "One", "respuesta": "Uno"},
            {"pregunta": "Two", "respuesta": "Dos"},
        ]
    }
    leccion = lecciones_data.get(leccion_id)
    if leccion:
        return jsonify(leccion)
    else:
        return jsonify({'error': 'Lección no encontrada'}), 404

@app.route('/api/audio/<texto>', methods=['GET'])
def get_audio(texto):
    try:
        # Generar audio con gTTS
        tts = gTTS(text=texto, lang='en')
        ruta_audio = f'/tmp/temp_audio_{random.randint(0, 100000)}.mp3'
        tts.save(ruta_audio)

        # Enviar el archivo
        return send_file(ruta_audio, as_attachment=True, mimetype='audio/mp3')
    except Exception as e:
        return jsonify({'error': f'Error al generar el audio: {str(e)}'}), 500

