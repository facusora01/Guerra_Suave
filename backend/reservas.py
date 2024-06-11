from datetime import datetime

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

def removerUUID(data):
    listaDatos = []
    for row in data:
        fila = dict(row)
        fila.pop("personaUUID")
        listaDatos.append(fila)
    return listaDatos