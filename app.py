from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors

from config import Config
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar MySQL
mysql = MySQL(app)

print('Leito-app: ', __name__)
print('Leito-connection: ', mysql.connection)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/check_connection')
def check_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        return jsonify({'message': 'Connection successful'})
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'Connection failed'}), 500

@app.route('/ping', methods=['GET'])
def ping():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id_producto, nombre, descripcion FROM producto")
        datos = cursor.fetchall()
        return jsonify({'Datos': datos})
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.route('/ping/<int:codigo>', methods=['GET'])
def leerCodigo(codigo):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id_producto, nombre, descripcion FROM producto WHERE id_producto = %s", (codigo,))
        datos = cursor.fetchone()
        if datos:
            return jsonify({'Datos': datos})
        else:
            return jsonify({'message': 'id no encontrado'}), 404
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.route('/ping', methods=['POST'])
def agregarDato():
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO producto (nombre, descripcion) VALUES (%s, %s)", 
                       (datos['nombre'], datos['descripcion']))
        mysql.connection.commit()
        return jsonify({'message': 'datos agregados correctamente'})
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.route('/ping/<int:codigo>', methods=['DELETE'])
def eliminarDato(codigo):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_producto FROM producto WHERE id_producto = %s", (codigo,))
        existe_dato = cursor.fetchone()

        if existe_dato:
            cursor.execute("DELETE FROM producto WHERE id_producto = %s", (codigo,))
            mysql.connection.commit()
            return jsonify({'message': 'Dato eliminado'})
        else:
            return jsonify({'message': 'El dato no existe o ya ha sido eliminado anteriormente'}), 404
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.route('/ping/<int:codigo>', methods=['PUT'])
def actualizarDato(codigo):
    try:
        datos = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE producto SET nombre = %s, descripcion = %s WHERE id_producto = %s", 
                       (datos['nombre'], datos['descripcion'], codigo))
        mysql.connection.commit()
        return jsonify({'message': 'Dato actualizado'})
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        datos = request.json
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM login WHERE usuario = %s AND passw = %s", 
                       (datos['usuario'], datos['passw']))
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Login successful', 'user': user['usuario']})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as error:
        print("An error occurred:", error)
        return jsonify({'message': 'error'}), 500

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada...</h1>", 404

if __name__ == "__main__":
    app.run()
