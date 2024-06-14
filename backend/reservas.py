from datetime import datetime

def superposicion_reservas(reservas, fecha_in, fecha_eg):

    lista_reservas = [dict(row) for row in reservas]

    date_format = '%Y-%m-%d'
    fecha_ingreso = datetime.strptime(fecha_in, date_format)
    fecha_egreso = datetime.strptime(fecha_eg, date_format)
    disponible = True

    for re in lista_reservas:
        if not fecha_ingreso <= re['fecha_ingreso'] and fecha_egreso <= re['fecha_ingreso']:
            disponible = False

        elif not fecha_ingreso >= re['fecha_egreso'] and fecha_egreso >= re['fecha_egreso']:
            disponible = False

        elif re['fecha_ingreso'] < fecha_ingreso < re['fecha_egreso']:
            disponible = False

        elif re['fecha_ingreso'] < fecha_egreso < re['fecha_egreso']:
            disponible = False

    return disponible


def fecha_valida(fecha_in, fecha_eg):

    fecha_valida = True

    if fecha_eg and fecha_in:
        date_format = '%Y-%m-%d'
        fecha_ingreso = datetime.strptime(fecha_in, date_format)
        fecha_egreso = datetime.strptime(fecha_eg, date_format)
        
        if fecha_egreso <= fecha_ingreso:
            fecha_valida = False
    
        if fecha_ingreso < datetime.now():
            fecha_valida = False
    
    return fecha_valida

def remover_UUID(data):
    lista_datos = []
    for row in data:
        fila = dict(row)
        fila.pop("persona_UUID")
        lista_datos.append(fila)
    return lista_datos