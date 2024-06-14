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

# PRE: Puede recibir un parámetro opcional 'error' en la query string.
# POST: Renderiza y devuelve la plantilla 'index.html'. Pasa el parámetro 'error' a la plantilla, si está presente.
@app.route('/')
def index():

    #Se renderiza la plantilla con el error si es que existe
    return render_template('index.html', error=request.args.get('error'))

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla 'restaurant.html'.
@app.route('/restaurant')
def restaurant():

    #Se renderiza la plantilla del restaurante
    return render_template('restaurant.html')

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla 'about.html'.
@app.route('/about')
def about():

    #Se renderiza la plantilla de about
    return render_template('about.html')

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla 'blog.html'.
@app.route('/blog')
def blog():

    #Se renderiza la plantilla de blog
    return render_template('blog.html')

# PRE: Puede recibir una solicitud GET o POST.
# POST: Renderiza y devuelve la plantilla 'contact.html' con las reseñas obtenidas. En caso de error, la lista de reseñas estará vacía.
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        #Si el request es GET, mostrara las reseñas
        if request.method == "GET":
            response = requests.get('http://127.0.0.1:5050/resenias')

        #Si el request es POST, se enviara la reseña
        elif request.method == "POST":
            email = request.form.get("email")
            cabaña = request.form.get("cabaña")
            puntuacion = request.form.get("puntuacion")
            comentario = request.form.get("reseña")
            data = {'email': email, 'cabaña': cabaña, 'puntuacion': puntuacion, 'comentario': comentario}
            response = requests.post('http://127.0.0.1:5050/resenias', json=data)

            return redirect(url_for('contact'))
        
    #Si el GET y POST fallan, se mostrara un mensaje de error
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

        #Se obtienen las reseñas
        result = response.json()
        reseñas = result['resenias']
        print(reseñas)
    except:
        reseñas = {'reseñas': []}

    #Se renderiza la plantilla con las reseñas
    return render_template('contact.html', Reseñas=reseñas)


# PRE: Recibe una solicitud POST con los datos 'fechaIngreso', 'fechaEgreso' y 'identificadorPosada'.
# POST: Redirige a 'misReservas' si la reserva es exitosa, o a 'obtenerPosada' con un mensaje de error si falla.
@app.route('/reservar', methods=["POST"])
def reservar():

    # Se recibe la info de la reserva
    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "fechaIngreso": request.form['fechaIngreso'],
        "fechaEgreso": request.form['fechaEgreso'],
        "identificadorPosada": request.form['identificadorPosada'],
    }

    # Se envía la info de la reserva
    response = requests.post('http://127.0.0.1:5050/reservas', json=data)


    # Si la respuesta es 200, se redirige a misReservas
    if(response.status_code == 200):
        return redirect(url_for('misReservas', correcta=True))
    
    # Si la respuesta es 400, se redirige a obtenerPosada con un mensaje de error
    return redirect(url_for('obtenerPosada', id=data['identificadorPosada'], fechaIngreso=data['fechaIngreso'], fechaEgreso=data['fechaEgreso'], error=response.json()['message']))

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla 'misreservas.html' con las reservas del usuario. Pasa la variable 'correcta' a la plantilla si está presente.
@app.route('/misreservas')
def misReservas():

    # Se hace la solicitud de las reservas del usuario
    response = requests.get('http://127.0.0.1:5050/reservas?email=p.lopez@gmail.com')
    response = response.json()

    # Se renderiza la plantilla con las reservas
    return render_template('misreservas.html', reservas=response['reservas'], correcta=request.args.get('correcta'))

# PRE: Recibe una solicitud POST con el dato 'idReserva'.
# POST: Elimina la reserva especificada y redirige a 'misReservas'.
@app.route('/cancelar', methods=['POST'])
def cancelarReserva():

    # Se recibe el id de la reserva a cancelar
    data = {
        "UUID": "69d07c33-1eec-11ef-bc3d-0242ac120002",
        "idReserva": int(request.form['idReserva'])
    }

    # Se envía la solicitud de cancelación
    requests.delete('http://127.0.0.1:5050/reservas', json=data)

    # Se redirige a misReservas
    return redirect(url_for('misReservas'))

# PRE: Recibe una solicitud GET con el parámetro 'id' en la URL. Puede recibir los parámetros opcionales 'fechaIngreso' y 'fechaEgreso'.
# POST: Renderiza y devuelve la plantilla 'posada.html' con la información de la posada y los parámetros 'fechas' y 'error' si están presentes.
@app.route('/posadas/<id>', methods=['GET'])
def obtenerPosada(id):

    # Se obtienen las fechas de ingreso y egreso
    fechas = {
        "fechaIngreso": request.args.get("fechaIngreso"),
        "fechaEgreso": request.args.get("fechaEgreso"),
    }

    # Se obtiene la información de la posada
    response = requests.get(f"""http://127.0.0.1:5050/posadas?identificador={id}""")
    posada = response.json()['posadas'][0]

    # Se realiza un split de la descripción de la posada, para una mejor visualización
    posada['descripcion'] = posada['descripcion'].split("-")
    posada['descripcion'] = filter(lambda x: x != "", posada['descripcion'])
    
    # Se renderiza la plantilla con la información de la posada
    return render_template('posada.html', posada=posada, reservable=True, fechas=fechas, error=request.args.get("error"))

# PRE: Recibe una solicitud POST con los datos de búsqueda de posadas.
# POST: Renderiza y devuelve la plantilla 'cabanas.html' con los resultados de la búsqueda. Si hay un error, redirige a 'index' con un mensaje de error.
@app.route('/buscar', methods=["POST"])
def buscarPosadas():

    # Se envía la solicitud de búsqueda de posadas
    response = requests.get('http://127.0.0.1:5050/posadas', params=request.form)
    
    # Se obtiene la respuesta
    data = response.json()

    # Si la respuesta no es 200, se redirige a index con un mensaje de error
    if response.status_code != 200:
        return redirect(url_for("index", error=data['message']))

    # Se renderiza la plantilla con los resultados de la búsqueda
    return render_template('cabanas.html', cabanas=data['posadas'], cantidad=data['cantidad'], filtros=data['filtros'])

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla 'cabanas.html' con todas las posadas disponibles.
@app.route('/cabanas', methods=["GET"])
def cabanas():

    # Se obtienen todas las posadas disponibles
    response = requests.get('http://127.0.0.1:5050/posadas')
    data = response.json()
    posadas = data['posadas']
    cantidad = data['cantidad']

    # Se renderiza la plantilla con las posadas
    return render_template('cabanas.html', cabanas=posadas, cantidad=cantidad, filtros={})

# PRE: Ninguna.
# POST: Renderiza y devuelve la plantilla '404.html' con un código de estado 404.
@app.errorhandler(404)
def error(e):

    #Se renderiza la plantilla de error 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)