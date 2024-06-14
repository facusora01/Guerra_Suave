from datetime import datetime

# PRE: Recibe una lista de reservas, una fecha de ingreso y una fecha de egreso.
# POST: Devuelve True si no hay superposición de reservas, False en caso contrario.
def superposicionReservas(reservas, fechaI, fechaE):

    listaReservas = [dict(row) for row in reservas]

    dateFormat = '%Y-%m-%d'
    fechaIngreso = datetime.strptime(fechaI, dateFormat)
    fechaEgreso = datetime.strptime(fechaE, dateFormat)
    disponible = True

    for re in listaReservas:
        if not fechaIngreso <= re['fechaIngreso'] and fechaEgreso <= re['fechaIngreso']:
            disponible = False

        elif not fechaIngreso >= re['fechaEgreso'] and fechaEgreso >= re['fechaEgreso']:
            disponible = False

        elif re['fechaIngreso'] < fechaIngreso < re['fechaEgreso']:
            disponible = False

        elif re['fechaIngreso'] < fechaEgreso < re['fechaEgreso']:
            disponible = False

    return disponible

# PRE: Recibe una fecha de ingreso y una fecha de egreso.
# POST: Devuelve True si la fecha de egreso es mayor a la fecha de ingreso y si la fecha de ingreso es mayor a la fecha actual, False en caso contrario.
def fechaValida(fechaI, fechaE):

    fechaValida = True

    if fechaE and fechaI:
        dateFormat = '%Y-%m-%d'
        fechaIngreso = datetime.strptime(fechaI, dateFormat)
        fechaEgreso = datetime.strptime(fechaE, dateFormat)
        
        if fechaEgreso <= fechaIngreso:
            fechaValida = False
    
        if fechaIngreso < datetime.now():
            fechaValida = False
    
    return fechaValida

# PRE: Recibe una lista de reservas.
# POST: Devuelve una lista de reservas sin el UUID de la persona.
def removerUUID(data):
    listaDatos = []
    for row in data:
        fila = dict(row)
        fila.pop("personaUUID")
        listaDatos.append(fila)
    return listaDatos