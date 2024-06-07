from flask import Flask, render_template, request, jsonify
import os
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

    Posadas = Lista_Cabanas['posadas']
    return render_template('index.html',posadas=Posadas)

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
    
    return render_template('Cabana_Amapola.html', posada=posada)

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


@app.route('/Cabanas', methods=["GET"])
def Cabanas():

    response = requests.get('http://127.0.0.1:5050/posadas')
    data = response.json()

    posadas = data['posadas']
    cantidad = data['cantidad']

    return render_template('Cabanas.html', cabanas=posadas, cantidad=cantidad)


@app.route("/conexion_a_reservas", methods=["GET"])
def conexion_a_reservas():
    response = requests.get('http://127.0.0.1:5050/reservas')
    data = response.json()

    reservas = data['reservas']
    cantidad = data['cantidad']

    return render_template("cone_a_rese.html", reservas=reservas, cantidad=cantidad)
    #return jsonify(data)

#error handler 404
@app.errorhandler(404)
# usar html Error_404.html
def error(e):
    return render_template('Error_404.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)