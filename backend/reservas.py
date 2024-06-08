from datetime import datetime

def superposicionReservas(reservas, fechaI, fechaE):

    listaReservas = [dict(row) for row in reservas]

    dateFormat = '%Y-%m-%d'
    fechaIngreso = datetime.strptime(fechaI, dateFormat)
    fechaEgreso = datetime.strptime(fechaE, dateFormat)
    fechaValida = True

    for re in listaReservas:
        if not fechaIngreso < re['fechaIngreso'] and fechaEgreso <= re['fechaIngreso']:
            fechaValida = False

        elif not fechaIngreso >= re['fechaEgreso'] and fechaEgreso > re['fechaEgreso']:
            fechaValida = False

        elif fechaEgreso <= fechaIngreso:
            fechaValida = False
      
        elif fechaIngreso < datetime.now():
            fechaValida = False
    
    return fechaValida

def removerUUID(data):
    listaDatos = []
    for row in data:
        fila = dict(row)
        fila.pop("personaUUID")
        listaDatos.append(fila)
    return listaDatos