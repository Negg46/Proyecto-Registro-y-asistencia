from flask import Flask, request, jsonify
from flask_cors import CORS
from Conexion import Registro_datos

app = Flask(__name__)
CORS(app)

registro = Registro_datos()

@app.route('/validar', methods=['POST'])
def validar():
    data = request.get_json(force=True) or {}
    dni = (data.get('identificacion') or data.get('dni') or '').strip()

    if not dni:
        return jsonify(status='error', message='Debe enviar la identificación del cliente.'), 400

    cliente = registro.obtener_cliente_por_dni(dni)
    if not cliente:
        return jsonify(status='not_found', message='Cliente no registrado. Por favor regístrese.'), 404

    info = registro.registrar_asistencia(dni)
    if not info:
        return jsonify(status='error', message='Error interno al registrar la asistencia.'), 500

    mensaje = (
        f"Bienvenido {cliente[1]}. Nivel actual: {info.get('nivel', 'Clasica')} - "
        f"Visitas este mes: {info.get('visitas_mes', 0)}."
    )
    if info.get('nivel') == 'VIP':
        mensaje += ' ¡Eres VIP!'

    return jsonify(status='success', message=mensaje, nivel=info.get('nivel'), visitas_mes=info.get('visitas_mes'))

if __name__ == '__main__':
    # Ejecutar con: python server.py
    app.run(host='0.0.0.0', port=5000)
