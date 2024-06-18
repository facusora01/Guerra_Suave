from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from reservas import superposicion_reservas, remover_UUID, fecha_valida
import sys

def create_connection(testing = False):
    password = "securepass"
    dbname = "posadasdb"
    port = 3306

    if len(sys.argv) > 1 or testing: 
        print("USING TESTING DB")
        port = 3309
        
    engine = create_engine(f"""mysql+pymysql://root:{password}@localhost:{port}/{dbname}""")

    try:
        connection = engine.connect()
    except SQLAlchemyError as err:
        print(err)
        exit()

    return connection

db_connection = create_connection()
app = Flask(__name__)


def run_query(query):
    db_connection.execute(text(query))
    db_connection.commit() 

def search_query(query):
    result = db_connection.execute(text(query))
    return result.mappings().all()


def filtros_posadas(args):
    filters = []

    if args.get('identificador'):
        try:
            identificador = int(args.get('identificador'))
            filters.append(f"identificador = {identificador}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para identificador'}), 400
    
    if args.get('camas_matrimoniales'):
        try:
            camas_matrimoniales = int(args.get('camas_matrimoniales'))
            filters.append(f"camas_matrimoniales >= {camas_matrimoniales}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para camas matrimoniales'}), 400

    if args.get('camas_individuales'):
        try:
            camas_individuales = int(args.get('camas_individuales'))
            filters.append(f"camas_individuales >= {camas_individuales}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para camas individuales'}), 400
    
    if args.get('precio_max'):
        try:
            precio_max = float(args.get('precio_max'))
            filters.append(f"precio_noche <= {precio_max}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para precio máximo'}), 400

    if args.get('precio_min'):
        try:
            precio_min = float(args.get('precio_min'))
            filters.append(f"precio_noche >= {precio_min}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para precio mínimo'}), 400

    if filters:
        return "WHERE " + " AND ".join(filters)
    else:
        return ""
    
def esta_disponible(args, posadas):
 
    posadas_validas = list(posadas)

    if args.get('fecha_ingreso') and args.get('fecha_egreso'):

        for posada in posadas:
            print(posada['identificador'])
            reservas = search_query(f"""SELECT * FROM reservas WHERE identificador_posada={posada['identificador']} """)
            if not superposicion_reservas(reservas, args['fecha_ingreso'], args['fecha_egreso']):
                posadas_validas.remove(posada)

    return posadas_validas

@app.route("/posadas")
def posadas():

    try:
        if not fecha_valida(request.args.get('fecha_ingreso'), request.args.get('fecha_egreso')):
            return jsonify({'message': 'La fecha debe ser en el futuro y en el orden correcto.'}), 400

        filters = filtros_posadas(request.args)
        result = search_query(f"""SELECT * FROM posadas {filters}""")
        posadas = [dict(row) for row in result]
        posadas = esta_disponible(request.args, posadas)
        return jsonify({'posadas': posadas, 'cantidad': len(posadas), 'filtros': request.args})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400
    

def obtener_reservas():   
    try:
        filters = ""

        if request.args.get('identificador_posada'):
            filters = f"""WHERE identificador_posada={request.args.get('identificador_posada')}"""

        elif request.args.get('email'):
            usuario = search_query(f"""SELECT * FROM usuarios WHERE email='{request.args.get('email')}' """)

            if not len(usuario):
                return jsonify({'message': 'Usuario inexistente'}), 400
   
            filters = f"""WHERE persona_UUID='{usuario[0]['UUID']}' """

        result = search_query(f"""SELECT * FROM reservas {filters}""")
        reservas = remover_UUID(result)
        return jsonify({'reservas': reservas, 'cantidad': len(reservas), 'filtros': request.args})
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400


def borrar_reserva():
    try:
        content = request.json

        reserva = search_query(f"""SELECT * FROM reservas WHERE id={content['id_reserva']}  """)
        if not len(reserva):
            return jsonify({'message': 'No existe la reserva'}), 400
        
        if not reserva[0]['persona_UUID'] == content['UUID']:
            return jsonify({'message': 'La reserva no pertenece al usuario'}), 400
        
        run_query(f"""DELETE FROM reservas WHERE id={content['id_reserva']} AND persona_UUID='{content['UUID']}' """)
        return jsonify({'message': "Reserva eliminada correctamente"})

    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'No se pudo borrar la reserva'}), 500


def crear_reserva():
    try:
        content = request.json

        posada = search_query(f"""SELECT * FROM posadas WHERE identificador={content['identificador_posada']}""")
        if not len(posada):
            return jsonify({'message': 'Posada inexistente'}), 400
        
        if not fecha_valida(content['fecha_ingreso'], content['fecha_egreso']):
            return jsonify({'message': 'La fecha debe ser en el futuro y en el orden correcto.'}), 400

        usuario = search_query(f"""SELECT * FROM usuarios WHERE UUID='{content['UUID']}' """)
        if not len(usuario):
            return jsonify({'message': 'Usuario inexistente'}), 400

        result = search_query(f"""SELECT * FROM reservas WHERE identificador_posada={content['identificador_posada']}""")
        if not superposicion_reservas(result, content['fecha_ingreso'], content['fecha_egreso']):
            return jsonify({'message': 'La fecha seleccionada para la reserva se encuentra ocupada.'}), 400
        
        run_query(f"""INSERT INTO reservas (identificador_posada, persona_UUID, fecha_ingreso, fecha_egreso, nombre_posada, imagen) VALUES ({content['identificador_posada']}, "{content['UUID']}", "{content['fecha_ingreso']}", "{content['fecha_egreso']}", "{posada[0]['nombre']}", "{posada[0]['foto1']}")""")
        return jsonify({'message': "Reserva correcta"})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'Error generando la reserva'}), 500
    except: 
        return jsonify({'message': 'Error en la solicitud.'}), 400


@app.route("/reservas", methods=["GET", "POST", "DELETE"])
def reservas():
    if request.method == "GET":
        return obtener_reservas()
    elif request.method == "POST":
        return crear_reserva()
    elif request.method == "DELETE":
        return borrar_reserva()

def obtener_resenias():
    try:
        result = search_query("""SELECT * FROM resenias""")
        resenias = [dict(row) for row in result]
        return jsonify({'resenias': resenias, 'cantidad': len(resenias)}), 200

    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400

def publicar_resenias():
    try:
        content = request.json
       
        mailUsuario = content['email']
        comentario = content['comentario']
        puntuacion = content['puntuacion']
        
        usuario = search_query(f"""SELECT * FROM usuarios WHERE email= '{mailUsuario}' """)

        if not usuario:
            return jsonify({'message': 'Usuario inexistente'}), 400        
        else:
            usuarioUUID = usuario[0]['UUID']
           
        posada = search_query(f"""SELECT * FROM posadas WHERE nombre = '{content['cabaña']}' """)

        if not posada:
            return jsonify({'message': 'Posada no encontrada'}), 400
        else:
            identificador_posada = posada[0]['identificador']

        run_query(f"""INSERT INTO resenias (identificador_posada, persona_UUID, puntuacion, comentario) VALUES ({identificador_posada}, '{usuarioUUID}', {puntuacion}, "{comentario}") """)
        return jsonify({'message': "Se ha agregado la reseña correctamente"}), 200
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'Error generando la reseña'}), 500
    except: 
        return jsonify({'message': 'Error en la solicitud.'}), 400

@app.route("/resenias", methods=["GET", "POST"])
def listar_resenias():
    if request.method == "GET":
        return obtener_resenias()
    if request.method == "POST":
        return publicar_resenias()
    
@app.errorhandler(404)
def error(e):
    return jsonify({'message': 'No encontrado'}), 404

if __name__ == "__main__":
    app.run(port=5050)