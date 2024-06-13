from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from reservas import superposicionReservas, removerUUID, fechaValida
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


def filtrosPosadas(args):
    filters = []

    if args.get('identificador'):
        try:
            identificador = int(args.get('identificador'))
            filters.append(f"identificador = {identificador}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para identificador'}), 400
    
    if args.get('camasMatrimoniales'):
        try:
            camasMatrimoniales = int(args.get('camasMatrimoniales'))
            filters.append(f"camasMatrimoniales >= {camasMatrimoniales}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para camas matrimoniales'}), 400

    if args.get('camasIndividuales'):
        try:
            camasIndividuales = int(args.get('camasIndividuales'))
            filters.append(f"camasIndividuales >= {camasIndividuales}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para camas individuales'}), 400
    
    if args.get('precioMax'):
        try:
            precioMax = float(args.get('precioMax'))
            filters.append(f"precioNoche <= {precioMax}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para precio máximo'}), 400

    if args.get('precioMin'):
        try:
            precioMin = float(args.get('precioMin'))
            filters.append(f"precioNoche >= {precioMin}")
        except ValueError:
            return jsonify({'message': 'Valor inválido para precio mínimo'}), 400

    if filters:
        return "WHERE " + " AND ".join(filters)
    else:
        return ""
    
def estaDisponible(args, posadas):
 
    posadasValidas = list(posadas)

    if args.get('fechaIngreso') and args.get('fechaEgreso'):

        for posada in posadas:
            print(posada['identificador'])
            reservas = search_query(f"""SELECT * FROM reservas WHERE identificadorPosada={posada['identificador']} """)
            if not superposicionReservas(reservas, args['fechaIngreso'], args['fechaEgreso']):
                posadasValidas.remove(posada)

    return posadasValidas

@app.route("/posadas")
def posadas():

    try:
        if not fechaValida(request.args.get('fechaIngreso'), request.args.get('fechaEgreso')):
            return jsonify({'message': 'La fecha debe ser en el futuro y en el orden correcto.'}), 400

        filters = filtrosPosadas(request.args)
        result = search_query(f"""SELECT * FROM posadas {filters}""")
        posadas = [dict(row) for row in result]
        posadas = estaDisponible(request.args, posadas)
        return jsonify({'posadas': posadas, 'cantidad': len(posadas), 'filtros': request.args})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400
    

def obtenerReservas():   
    try:
        filters = ""

        if request.args.get('identificadorPosada'):
            filters = f"""WHERE identificadorPosada={request.args.get('identificadorPosada')}"""

        elif request.args.get('email'):
            usuario = search_query(f"""SELECT * FROM usuarios WHERE email='{request.args.get('email')}' """)

            if not len(usuario):
                return jsonify({'message': 'Usuario inexistente'}), 400
   
            filters = f"""WHERE personaUUID='{usuario[0]['UUID']}' """

        result = search_query(f"""SELECT * FROM reservas {filters}""")
        reservas = removerUUID(result)
        return jsonify({'reservas': reservas, 'cantidad': len(reservas), 'filtros': request.args})
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400


def borrarReserva():
    try:
        content = request.json
        print(content)
        
        reserva = search_query(f"""SELECT * FROM reservas WHERE id={content['idReserva']}  """)
        if not len(reserva):
            return jsonify({'message': 'No existe la reserva'}), 400
        
        if not reserva[0]['personaUUID'] == content['UUID']:
            return jsonify({'message': 'La reserva no pertenece al usuario'}), 400
        
        run_query(f"""DELETE FROM reservas WHERE id={content['idReserva']} AND personaUUID='{content['UUID']}' """)
        return jsonify({'message': "Reserva eliminada correctamente"})

    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'No se pudo borrar la reserva'}), 500


def crearReserva():
    try:
        content = request.json

        posada = search_query(f"""SELECT * FROM posadas WHERE identificador={content['identificadorPosada']}""")
        if not len(posada):
            return jsonify({'message': 'Posada inexistente'}), 400
        
        if not fechaValida(content['fechaIngreso'], content['fechaEgreso']):
            return jsonify({'message': 'La fecha debe ser en el futuro y en el orden correcto.'}), 400

        usuario = search_query(f"""SELECT * FROM usuarios WHERE UUID='{content['UUID']}' """)
        if not len(usuario):
            return jsonify({'message': 'Usuario inexistente'}), 400

        result = search_query(f"""SELECT * FROM reservas WHERE identificadorPosada={content['identificadorPosada']}""")
        if not superposicionReservas(result, content['fechaIngreso'], content['fechaEgreso']):
            return jsonify({'message': 'La fecha seleccionada para la reserva se encuentra ocupada.'}), 400
        
        run_query(f"""INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso, nombrePosada, imagen) VALUES ({content['identificadorPosada']}, "{content['UUID']}", "{content['fechaIngreso']}", "{content['fechaEgreso']}", "{posada[0]['nombre']}", "{posada[0]['foto1']}")""")
        return jsonify({'message': "Reserva correcta"})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'Error generando la reserva'}), 500
    except: 
        return jsonify({'message': 'Error en la solicitud.'}), 400


@app.route("/reservas", methods=["GET", "POST", "DELETE"])
def reservas():
    if request.method == "GET":
        return obtenerReservas()
    elif request.method == "POST":
        return crearReserva()
    elif request.method == "DELETE":
        return borrarReserva()

def obtenerResenias():
    try:
        result = search_query("""SELECT * FROM resenias""")
        resenias = [dict(row) for row in result]
        return jsonify({'resenias': resenias, 'cantidad': len(resenias)}), 200

    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400

def publicarResenias():
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
            identificadorPosada = posada[0]['identificador']

        run_query(f"""INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES ({identificadorPosada}, '{usuarioUUID}', {puntuacion}, "{comentario}") """)
        return jsonify({'message': "Se ha agregado la reseña correctamente"}), 200
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'Error generando la reseña'}), 500
    except: 
        return jsonify({'message': 'Error en la solicitud.'}), 400

@app.route("/resenias", methods=["GET", "POST"])
def listarResenias():
    if request.method == "GET":
        return obtenerResenias()
    if request.method == "POST":
        return publicarResenias()
    
@app.errorhandler(404)
def error(e):
    return jsonify({'message': 'No encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5050)