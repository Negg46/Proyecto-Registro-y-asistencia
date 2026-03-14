import mysql.connector

# Configuración de la conexión (igual que en Conexion.py)
conexion = mysql.connector.connect(
    host='localhost',
    database='registro_casino',  # Si no existe, lo crearemos
    user='root',
    password='',  # Cambia si tienes contraseña
)

cursor = conexion.cursor()

# Leer y ejecutar el archivo SQL
with open('registro_casino.sql', 'r', encoding='utf-8') as file:
    sql_script = file.read()

# Ejecutar el script SQL (dividir por ; si es necesario, pero el dump ya está bien)
try:
    # Ejecutar el script completo
    for statement in sql_script.split(';'):
        if statement.strip():
            cursor.execute(statement)
    conexion.commit()
    print("✅ Base de datos importada correctamente con datos de ejemplo.")
except Exception as e:
    print(f"❌ Error al importar: {e}")
finally:
    cursor.close()
    conexion.close()