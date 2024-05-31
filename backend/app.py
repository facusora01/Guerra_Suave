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
 


@app.errorhandler(404)
def error(e):
    return jsonify({'message': 'No encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5050)