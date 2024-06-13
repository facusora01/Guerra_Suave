import unittest
import requests 
import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def search_query(query):
    result = db_connection.execute(text(query))
    return result.mappings().all()

def create_connection():
    password = "securepass"
    dbname = "posadasdb"
    port = 3309
        
    engine = create_engine(f"""mysql+pymysql://root:{password}@localhost:{port}/{dbname}""")

    try:
        connection = engine.connect()
    except SQLAlchemyError as err:
        print(err)
        exit()

    return connection

db_connection = create_connection()


class TestApisUnicas(unittest.TestCase):

    def testObtenerPosadas(self):
        response = requests.get('http://127.0.0.1:5050/posadas').json()
        self.assertEqual(response['cantidad'], 6)

    def testObtenerPosadasFiltroCamasI(self):
        response = requests.get('http://127.0.0.1:5050/posadas?camasIndividuales=5').json()
        self.assertEqual(response['cantidad'], 2)

    def testObtenerPosadasFiltroCamasM(self):
        response = requests.get('http://127.0.0.1:5050/posadas?camasMatrimoniales=3').json()
        self.assertEqual(response['cantidad'], 0)

    def testObtenerReservas(self):
        response = requests.get('http://127.0.0.1:5050/reservas').json()
        self.assertGreaterEqual(response['cantidad'], 2)

    def testObtenerReservasUsuario(self):
        response = requests.get('http://127.0.0.1:5050/reservas?email=p.lopez@gmail.com').json()
        self.assertGreaterEqual(response['reservas'][0]['identificadorPosada'], 101)

    def testReservaUsuarioInexistente(self):
        data = {
            "UUID": "3456-789a-b2cd-e12345678901",
            "identificadorPosada": 201,
            "fechaIngreso": (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "fechaEgreso": (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        }
        reservaResponse = requests.post('http://127.0.0.1:5050/reservas', json=data)    
        self.assertEqual(reservaResponse.json()['message'], 'Usuario inexistente')

    def testReservaPosadaInexistente(self):
        data = {
            "UUID": "789a01bc-3456-789a-b2cd-e12345678901",
            "identificadorPosada": 801,
            "fechaIngreso": (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "fechaEgreso": (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        }
        reservaResponse = requests.post('http://127.0.0.1:5050/reservas', json=data)    
        self.assertEqual(reservaResponse.json()['message'], 'Posada inexistente')

    def testReservaFechaIncorrecta(self):
        data = {
            "UUID": "789a01bc-3456-789a-b2cd-e12345678901",
            "identificadorPosada": 201,
            "fechaIngreso": (datetime.date.today() - datetime.timedelta(days=20)).strftime('%Y-%m-%d'),
            "fechaEgreso": (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        }
        reservaResponse = requests.post('http://127.0.0.1:5050/reservas', json=data)    
        self.assertEqual(reservaResponse.json()['message'], 'La fecha debe ser en el futuro y en el orden correcto.')



class TestFlow(unittest.TestCase):

    def testGenerarEliminarReserva(self):

        with self.subTest():
            data = {
                "UUID": "789a01bc-3456-789a-b2cd-e12345678901",
                "identificadorPosada": 201,
                "fechaIngreso": (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                "fechaEgreso": (datetime.date.today() + datetime.timedelta(days=5)).strftime('%Y-%m-%d')
            }
    
            reservaResponse = requests.post('http://127.0.0.1:5050/reservas', json=data)
            self.assertEqual(reservaResponse.status_code, 200)

        with self.subTest():
            reservas = search_query(f"""SELECT * FROM reservas WHERE personaUUID='789a01bc-3456-789a-b2cd-e12345678901' """)
            self.assertEqual(reservas[0]['fechaIngreso'].date(), (datetime.date.today() + datetime.timedelta(days=1)))
        
        with self.subTest():
            response = requests.get('http://127.0.0.1:5050/reservas?email=maria.gomez@hotmail.com').json()

            data = {
                "UUID": "789a01bc-3456-789a-b2cd-e12345678901",
                "idReserva": response['reservas'][0]['id']
            }

            requests.delete('http://127.0.0.1:5050/reservas', json=data).json()

            response2 = requests.get('http://127.0.0.1:5050/reservas?email=maria.gomez@hotmail.com').json()
            # reservas = search_query(f"""SELECT * FROM reservas WHERE id={response['reservas'][0]['id']} """)

            self.assertEqual(len(response2['reservas']), 0)

        
    def testGenerarResenia(self):

        cantidadOriginal = requests.get('http://127.0.0.1:5050/resenias').json()['cantidad']
        
        data = {
            "email": "p.lopez@gmail.com",
            "comentario": f"""Increible {cantidadOriginal}""",
            "puntuacion": 4,
            "cabaña": "Amapola"
        }

        requests.post('http://127.0.0.1:5050/resenias', json=data)

        response = requests.get('http://127.0.0.1:5050/resenias').json()
        self.assertEqual(cantidadOriginal + 1, response['cantidad'])
      
        
if __name__ == '__main__':
    unittest.main()