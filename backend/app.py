from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

def create_connection():
    password = "securepass"
    dbname = "posadasdb"
    port = 3306
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


def removerUUID(data):
    listaDatos = []
    for row in data:
        fila = dict(row)
        fila.pop("personaUUID")
        listaDatos.append(fila)
    return listaDatos


def filtrosPosadas(args):
    # if(request.args):
    #     filters = "WHERE"
    #     for arg in request.args:
    #         filters += f""" {arg}={request.args.get(arg)} AND"""
    #     filters = filters[:-3]
    return ""

@app.route("/posadas")
def posadas():

    try:
        filters = filtrosPosadas(request.args)
        result = search_query(f"""SELECT * FROM posadas {filters}""")
        posadas = [dict(row) for row in result]
        return jsonify({'posadas': posadas, 'cantidad': len(posadas)})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400
    
    
@app.route("/reservas")
def reservas():

    filters = ""
   
    try:
        if request.args.get('identificadorPosada'):
            filters = f"""WHERE identificadorPosada={request.args.get('identificadorPosada')}"""

        elif request.args.get('email'):
            usuario = search_query(f"""SELECT * FROM usuarios WHERE email='{request.args.get('email')}' """)

            if not len(usuario):
                return jsonify({'message': 'Usuario inexistente'}), 400
   
            filters = f"""WHERE personaUUID='{usuario[0]['UUID']}' """

        result = search_query(f"""SELECT * FROM reservas {filters}""")
        reservas = removerUUID(result)
        return jsonify({'reservas': reservas, 'cantidad': len(reservas)})
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': "Error en la solicitud"}), 400


@app.route("/reservar", methods=["POST"])
def reservar():

    try:
        content = request.json

        if not len(search_query(f"""SELECT * FROM posadas WHERE identificador={content['identificadorPosada']}""")):
            return jsonify({'message': 'Posada inexistente1'}), 400
        
        usuario = search_query(f"""SELECT * FROM usuarios WHERE UUID='{content['UUID']}' """)
        if not len(usuario):
            return jsonify({'message': 'Usuario inexistente'}), 400

        result = search_query(f"""SELECT * FROM reservas WHERE identificadorPosada={content['identificadorPosada']}""")
        reservas = [dict(row) for row in result]

        dateFormat = '%Y-%m-%d'
        fechaIngreso = datetime.strptime(content['fechaIngreso'], dateFormat)
        fechaEgreso = datetime.strptime(content['fechaEgreso'], dateFormat)
        fechaValida = True

        for re in reservas:
            if re['fechaIngreso'] <= fechaIngreso and re['fechaEgreso'] > fechaIngreso:
                fechaValida = False

            elif re['fechaIngreso'] < fechaEgreso and re['fechaEgreso'] >= fechaEgreso:
                fechaValida = False

            elif fechaEgreso <= fechaIngreso:
                fechaValida = False

            elif fechaIngreso < datetime.now():
                fechaValida = False

        if not fechaValida:
            return jsonify({'message': 'La fecha seleccionada para la reseva no es valida.'}), 400
        
        print("B")

        run_query(f"""INSERT INTO reservas VALUES ({content['identificadorPosada']}, "{content['UUID']}", "{content['fechaIngreso']}", "{content['fechaEgreso']}")""")
        return jsonify({'message': "Reserva correcta"})
    
    except SQLAlchemyError as err:
        print(err)
        return jsonify({'message': 'Error generando la reserva'}), 500
    except: 
        return jsonify({'message': 'Error en la solicitud.'}), 400


@app.errorhandler(404)
def error(e):
    return jsonify({'message': 'No encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5050)