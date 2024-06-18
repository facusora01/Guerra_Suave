from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from requests.exceptions import ConnectionError

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', error=request.args.get('error'))


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
        "fecha_ingreso": request.form['fecha_ingreso'],
        "fecha_egreso": request.form['fecha_egreso'],
        "identificador_posada": request.form['identificador_posada'],
    }

    response = requests.post('http://127.0.0.1:5050/reservas', json=data)

    if(response.status_code == 200):
        return redirect(url_for('mis_reservas', correcta=True))
    
    return redirect(url_for('obtener_posada', id=data['identificador_posada'], fecha_ingreso=data['fecha_ingreso'], fecha_egreso=data['fecha_egreso'], error=response.json()['message']))


@app.route('/mis_reservas')
def mis_reservas():
    response = requests.get('http://127.0.0.1:5050/reservas?email=p.lopez@gmail.com')
    response = response.json()
    return render_template('mis_reservas.html', reservas=response['reservas'], correcta=request.args.get('correcta'))


@app.route('/cancelar', methods=['POST'])
def cancelar_reserva():

    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "id_reserva": int(request.form['id_reserva'])
    }

    requests.delete('http://127.0.0.1:5050/reservas', json=data)
    return redirect(url_for('mis_reservas'))


@app.route('/posadas/<id>', methods=['GET'])
def obtener_posada(id):
    fechas = {
        "fecha_ingreso": request.args.get("fecha_ingreso"),
        "fecha_egreso": request.args.get("fecha_egreso"),
    }
    response = requests.get(f"""http://127.0.0.1:5050/posadas?identificador={id}""")
    posada = response.json()['posadas'][0]
    posada['descripcion'] = posada['descripcion'].split("-")
    posada['descripcion'] = filter(lambda x: x != "", posada['descripcion'])
  
    return render_template('posada.html', posada=posada, reservable=True, fechas=fechas, error=request.args.get("error"))


@app.route('/buscar', methods=["POST"])
def buscar_posadas():
    response = requests.get('http://127.0.0.1:5050/posadas', params=request.form)
    
    data = response.json()
    if response.status_code != 200:
        return redirect(url_for("index", error=data['message']))

    return render_template('cabanas.html', cabanas=data['posadas'], cantidad=data['cantidad'], filtros=data['filtros'])


@app.route('/cabanas', methods=["GET"])
def cabanas():
    response = requests.get('http://127.0.0.1:5050/posadas')
    data = response.json()
    posadas = data['posadas']
    cantidad = data['cantidad']
    return render_template('cabanas.html', cabanas=posadas, cantidad=cantidad, filtros={})


@app.errorhandler(404)
def error(e):
    return render_template('404.html'), 404

@app.errorhandler(ConnectionError)
def internal_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(port=5000)