"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as m
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.Algorithms.Sorting import customsort as cus
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_catalog():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    catalog = {'Trabajos': None,
               'mapa_id': None,
               'dateIndex': None,
               'habilidades_id': None,
               'habilidades_name': None,
               'employment_types_id': None,
               'multilocations_id': None,}
    
    # Lista con todos los trabajos encontrados en el archivo de carga
    catalog['Trabajos'] = lt.newList('ARRAY_LIST', compareJobIds)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                     cmpfunction=compareDates)
    catalog['sizeIndex'] = om.newMap(omaptype='RBT',
                                     cmpfunction=compareSizes)
    catalog['mapa_id'] = m.newMap(300000,
                                  maptype='PROBING',
                                  loadfactor=0.7)


    # EStructuras de datos para guardar info del csv skills
    catalog["habilidades_id"] = m.newMap(10000,
                                          maptype="CHAINING",
                                          loadfactor = 4) 
    # EStructuras de datos para guardar info del csv emlpoyment types
    catalog['employment_types_id'] = m.newMap(10000,
                                               maptype = "CHAINING",
                                               loadfactor = 4)
    catalog['salary_min'] = om.newMap(omaptype='RBT',
                                      cmpfunction=compareSalary)
    
    # EStructuras de datos para guardar info del csv multilocation
    catalog['multilocations_id'] = m.newMap(10000,
                                               maptype = "CHAINING",
                                               loadfactor = 4)
    return catalog


# Funciones para agregar informacion al modelo

def add_data_jobs(catalog, job):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(catalog['Trabajos'], job)
    update_date_index(catalog['dateIndex'], job)
    return catalog

def update_date_index(map, job):
    """
    Se toma la fecha del trabajo y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    fecha = job["published_at"]
    fecha_f = datetime.datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%fZ")
    entry = om.get(map, fecha_f.date())
    if entry is None:
        datentry = new_data_entry(job)
        om.put(map, fecha_f.date(), datentry)
    else:
        datentry = me.getValue(entry)
    add_date_index(datentry, job)
    return map

def add_date_index(datentry, job):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry["lstjobs"]
    lt.addLast(lst, job)
    cityIndex = datentry["cityIndex"]
    cityentry = m.get(cityIndex, job["city"])
    if (cityentry is None):
        entry = new_city_entry(job["city"], job)
        lt.addLast(entry["lstcity"], job) #
        m.put(cityIndex, job["city"], entry)
    else:
        entry = me.getValue(cityentry)
        lt.addLast(entry["lstcity"], job) #
    return datentry

def new_data_entry(job):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {"lstjobs": None,
             "cityIndex": None, 
             "countryIndex": None}
    entry["cityIndex"] = m.newMap(numelements=30,
                                     maptype="PROBING",
                                     cmpfunction=compareOffenses)
    entry["lstjobs"] = lt.newList("ARRAY_LIST", compareDates)
    lt.addLast(entry["lstjobs"], job)
    return entry

def new_city_entry(city, job):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    entry = {"city": None, "lstcity": None}
    entry["city"] = city
    entry["lstcity"] = lt.newList("SINGLE_LINKED", compareDates)
    lt.addLast(entry["lstcity"], job)
    return entry

def add_skills(catalog, skill):
    add_skills_id(catalog, skill['id'], skill)
    
def add_skills_id(catalog, id, skill):
    skills = catalog['habilidades_id']
    existid = m.contains(skills, id)
    if existid:
        entry = m.get(skills, id)
        skillid = me.getValue(entry)
    else:
        skillid = new_skill_id(id)
        m.put(skills, id, skillid)
    lt.addLast(skillid['row'],skill)
    
    skillid['sum'] += int(skill['level'])
    skillid['size'] += 1
    skillid['avg'] = int(skillid['sum'])/int(skillid['size'])

def new_skill_id(id):
    skill_id = {'id': "",
                "row": None, #Columnas enteras con el id - name;level;id
                'sum': 0, #Suma de los niveles de las habilidades
                'size': 0, # conteo de numero de habilidades
                'avg': 0 #Promedio de habilidades
                }

    skill_id['id'] = id
    skill_id['row'] = lt.newList('ARRAY_LIST')
    return skill_id

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(catalog, initialDate, finalDate):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    # TODO: Realizar el requerimiento 1
    names = []
    lst = om.values(catalog["dateIndex"], initialDate, finalDate)
    lst_flt = lt.newList('ARRAY_LIST', compareDates) #REVISAR CON Y SIN CMP - BUSCAR CAMBIOS EN FECHAS
    skills_flt = lt.newList('ARRAY_LIST')
    for lstdate in lt.iterator(lst):
        for job in lt.iterator(lstdate['lstjobs']):
            lt.addLast(lst_flt, job)
        
    size = lt.size(lst_flt)
    
    if lst_flt != 0:
        lst_flt = sa.sort(lst_flt, cmp_fecha_empresa) # REVISAR ALGORITMO DE SORT
    
    for job in lt.iterator(lst_flt):
        skill_map = me.getValue(m.get(catalog['habilidades_id'],job['id']))
        for row in lt.iterator(skill_map['row']):
            names.append(row['name'])
        lt.addLast(skills_flt, names)
        names = []  
    catalog['REQ1'] = [lst_flt, skills_flt]

    return catalog, size


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass

def select_data_size(algo_opt):
    """
    Función para escoger el tipo de archivo con el que se ejecuta el programa
    """
    #Rta por defecto
    DataSize = 10
    Sizemsg = "Se escogió por defecto la opción 10 - small"
    
    if algo_opt == 1:
        DataSize = "10-por-"
        Sizemsg = "Se ha escogido el tamaño 10-por"
        
    elif algo_opt == 2:
        DataSize = "20-por-"
        Sizemsg = "Se ha escogido el tamaño 20-por"

    elif algo_opt == 3:
        DataSize = "30-por-"
        Sizemsg = "Se ha escogido el tamaño 30-por"

    elif algo_opt == 4:
        DataSize = "40-por-"
        Sizemsg = "Se ha escogido el tamaño 40-por"
        
    elif algo_opt == 5:
        DataSize = "50-por-"
        Sizemsg = "Se ha escogido el tamaño 50-por"
        
    elif algo_opt == 6:
        DataSize = "60-por-"
        Sizemsg = "Se ha escogido el tamaño 60-por"
        
    elif algo_opt == 7:
        DataSize = "70-por-"
        Sizemsg = "Se ha escogido el tamaño 70-por"
        
    elif algo_opt == 8:
        DataSize = "80-por-"
        Sizemsg = "Se ha escogido el tamaño 80-por"
        
    elif algo_opt == 9:
        DataSize = "90-por-"
        Sizemsg = "Se ha escogido el tamaño 90-por"
        
    elif algo_opt == 10:
        DataSize = "small-"
        Sizemsg = "Se ha escogido el tamaño small-"
        
    elif algo_opt == 11:
        DataSize = "medium-"
        Sizemsg = "Se ha escogido el tamaño medium-"
        
    elif algo_opt == 12:
        DataSize = "large-"
        Sizemsg = "Se ha escogido el tamaño large-"
    return DataSize, Sizemsg


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

def compareJobIds(id1, id2):
    """
    Compara dos ids de dos trabajos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1
    
def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
def compareSizes(date1, date2): # COMPLETAR
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareSalary(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(list, cmp):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    return cus.sort(list, cmp)

def cmp_fecha_empresa(oferta1, oferta2): #Criterio ordenamiento RQ 5 - Fecha mayor a menor, si igual, nombre de empresa de A-Z
    if (datetime.datetime.strptime(oferta1["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ") > datetime.datetime.strptime(oferta2["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")):
        return True
    elif (datetime.datetime.strptime(oferta1["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ") == datetime.datetime.strptime(oferta2["published_at"],"%Y-%m-%dT%H:%M:%S.%fZ")):
        if (oferta1["company_name"] <= oferta2["company_name"]):
            return True
        else: return False
    else: return False
