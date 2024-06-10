from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
import requests

app = Flask(__name__)

#activar debugger

'''
ESTO ES PARA QUE EL DEBUGGER SE ACTIVE AUTOMATICAMENTE
============================================================
============================================================
''' 
os.environ['FLASK_DEBUG'] = '1'
'''
============================================================
============================================================
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Amapola', methods=['GET'])
def Amapola():
    try:
        response = requests.get('http://127.0.0.1:5050/posadas')
        Lista_Cabanas = response.json()
    except requests.exceptions.RequestException as error:
        print("=====================================")
        print(f"Error en la solicitud: {error}")
        print("=====================================")
        Lista_Cabanas = {'posadas': []}  # Inicializar con una lista vacía en caso de error
    except ValueError as error:
        print("=====================================")
        print(f"Error al decodificar JSON: {error}")
        print("=====================================")
        Lista_Cabanas = {'posadas': []}  # Inicializar con una lista vacía en caso de error

    posada = None
    for cabana in Lista_Cabanas['posadas']:
        if cabana['identificador'] == 201:  # Cambia el identificador por el que necesites
            posada = cabana
            break
    
    return render_template('posada.html', posada=posada)

@app.route('/Carpincho')
def Carpincho():
    return render_template('Cabana_Carpincho.html')

@app.route('/Ciervo_Blanco')
def Ciervo_Blanco():
    return render_template('Cabana_Ciervo_Blanco.html')

@app.route('/Hierba_Alta')
def Hierba_Alta():
    return render_template('Cabana_Hierba_Alta.html')

@app.route('/Bosque_Alto')
def Bosque_Alto():
    return render_template('Cabana_Bosque_Alto.html')

@app.route('/Trucha_Dorada')
def Trucha_Dorada():
    return render_template('Cabana_Trucha_Dorada.html')

@app.route('/blog_single')
def blog_single():
    return render_template('blog_single.html')

### Reservas
@app.route('/reservar', methods=["POST"])
def reservar():

    print(request.form)
    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "fechaIngreso": request.form['fechaIngreso'],
        "fechaEgreso": request.form['fechaEgreso'],
        "identificadorPosada": request.form['identificadorPosada'],
    }

    print(data)

    response = requests.post('http://127.0.0.1:5050/reservas', json=data)
    
    print(response)
    if(response.status_code == 200):
        return redirect(url_for('misReservas'))
    
    return redirect(url_for('misReservas'))

@app.route('/misreservas')
def misReservas():
    response = requests.get('http://127.0.0.1:5050/reservas?email=p.lopez@gmail.com')
    response = response.json()
    return render_template('misreservas.html', reservas=response['reservas'])

@app.route('/cancelar', methods=['POST'])
def cancelarReserva():

    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "idReserva": int(request.form['idReserva'])
    }

    requests.delete('http://127.0.0.1:5050/reservas', json=data)
    return redirect(url_for('misReservas'))
###

@app.route('/posadas/<id>', methods=['GET'])
def obtenerPosada(id):
    response = requests.get(f"""http://127.0.0.1:5050/posadas?identificador={id}""")
    posada = response.json()['posadas'][0]
    return render_template('posada.html', posada=posada, reservable=True)

@app.route('/buscar', methods=["POST"])
def buscarPosadas():
    response = requests.get('http://127.0.0.1:5050/posadas', params=request.form)
    data = response.json()
    return render_template('Cabanas.html', cabanas=data['posadas'], cantidad=data['cantidad'], filtros=data['filtros'])


@app.route('/Cabanas', methods=["GET"])
def Cabanas():
    response = requests.get('http://127.0.0.1:5050/posadas')
    data = response.json()
    posadas = data['posadas']
    cantidad = data['cantidad']
    return render_template('Cabanas.html', cabanas=posadas, cantidad=cantidad, filtros={})


@app.route("/conexion_a_reservas", methods=["GET"])
def conexion_a_reservas():
    response = requests.get('http://127.0.0.1:5050/reservas')
    data = response.json()

    reservas = data['reservas']
    cantidad = data['cantidad']

    return render_template("cone_a_rese.html", reservas=reservas, cantidad=cantidad)
    #return jsonify(data)

@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)