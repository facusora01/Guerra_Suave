from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    return render_template('index.html', error=request.args.get('error'))

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == "GET":
            response = requests.get('http://127.0.0.1:5050/resenias')
        elif request.method == "POST":
            email = request.form.get("email")
            cabaña = request.form.get("cabaña")
            puntuacion = request.form.get("puntuacion")
            comentario = request.form.get("reseña")
            data = {'email': email, 'cabaña': cabaña, 'puntuacion': puntuacion, 'comentario': comentario}
            response = requests.post('http://127.0.0.1:5050/resenias', json=data)
            return redirect(url_for('contact'))
    except requests.exceptions.RequestException as error:
        print("=====================================")
        print(f"Error en la solicitud: {error}")
        print("=====================================")
        reseñas = {'reseñas': []}  # Inicializar con una lista vacía en caso de error
    except ValueError as error:
        print("=====================================")
        print(f"Error al decodificar JSON: {error}")
        print("=====================================")
        reseñas = {'reseñas': []}  # Inicializar con una lista vacía en caso de error
    try:
        result = response.json()
        reseñas = result['resenias']
        print(reseñas)
    except:
        reseñas = {'reseñas': []}
    return render_template('contact.html', Reseñas=reseñas)

@app.route('/blog_single')
def blog_single():
    return render_template('blog_single.html')


@app.route('/reservar', methods=["POST"])
def reservar():

    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "fechaIngreso": request.form['fechaIngreso'],
        "fechaEgreso": request.form['fechaEgreso'],
        "identificadorPosada": request.form['identificadorPosada'],
    }

    response = requests.post('http://127.0.0.1:5050/reservas', json=data)

    if(response.status_code == 200):
        return redirect(url_for('misReservas', correcta=True))
    
    return redirect(url_for('obtenerPosada', id=data['identificadorPosada'], fechaIngreso=data['fechaIngreso'], fechaEgreso=data['fechaEgreso'], error=response.json()['message']))


@app.route('/misreservas')
def misReservas():
    response = requests.get('http://127.0.0.1:5050/reservas?email=p.lopez@gmail.com')
    response = response.json()
    return render_template('misreservas.html', reservas=response['reservas'], correcta=request.args.get('correcta'))


@app.route('/cancelar', methods=['POST'])
def cancelarReserva():

    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "idReserva": int(request.form['idReserva'])
    }

    requests.delete('http://127.0.0.1:5050/reservas', json=data)
    return redirect(url_for('misReservas'))


@app.route('/posadas/<id>', methods=['GET'])
def obtenerPosada(id):
    fechas = {
        "fechaIngreso": request.args.get("fechaIngreso"),
        "fechaEgreso": request.args.get("fechaEgreso"),
    }
    response = requests.get(f"""http://127.0.0.1:5050/posadas?identificador={id}""")
    posada = response.json()['posadas'][0]
    posada['descripcion'] = posada['descripcion'].split("-")
    posada['descripcion'] = filter(lambda x: x != "", posada['descripcion'])
  
    return render_template('posada.html', posada=posada, reservable=True, fechas=fechas, error=request.args.get("error"))


@app.route('/buscar', methods=["POST"])
def buscarPosadas():
    response = requests.get('http://127.0.0.1:5050/posadas', params=request.form)
    
    data = response.json()
    if response.status_code != 200:
        return redirect(url_for("index", error=data['message']))

    return render_template('Cabanas.html', cabanas=data['posadas'], cantidad=data['cantidad'], filtros=data['filtros'])


@app.route('/Cabanas', methods=["GET"])
def Cabanas():
    response = requests.get('http://127.0.0.1:5050/posadas')
    data = response.json()
    posadas = data['posadas']
    cantidad = data['cantidad']
    return render_template('Cabanas.html', cabanas=posadas, cantidad=cantidad, filtros={})


@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)