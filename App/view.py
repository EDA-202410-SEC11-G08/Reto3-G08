"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control, memflag):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    ans = controller.load_data(control, memflag)
    return ans


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    print("\nBuscando ofertas en un rango de fechas: ")
    initialDate = input("Fecha Inicial (YYYY-MM-DD): ")
    finalDate = input("Fecha Final (YYYY-MM-DD): ")
    total = controller.req_1(control, initialDate, finalDate)
    print("\nTotal de ofertas pulicadas en el rango de fechas: " + str(total))
    if total > 10: 
        num = total
        table1, table2 = printTableJobs(control["model"]["Trabajos"], int(10))
        print('Primeras ' + str(10) + " Ofertas")
        print(tabulate(table1))
        print('Ultimas ' + str(10) + " Ofertas")
        print(tabulate(table2))   
    else:
        num =total
        table3=printTableJobs1(control["model"]["Trabajos"], int(num))
        print(table3)
            

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def printTableJobs1(list, num):
    table1 = []
    header = ['Oferta','Empresa','Experticia','Publicación','País','Ciudad']
    table1.append(header)
    jobs1 = lt.subList(list, 1, num)

    for job in lt.iterator(jobs1):
        table1.append([job['title'],
        job['company_name'],
        job['experience_level'],
        job['published_at'],
        job['country_code'],
        job['city']])


        
    return table1

# IMPRIMIR TABLAS
def printTableJobs(list, num):
    table1 = []
    table2 = []
    header = ['Oferta','Empresa','Experticia','Publicación','País','Ciudad']
    table1.append(header)
    table2.append(header)
    jobs1 = lt.subList(list, 1, num)
    jobs2 = lt.subList(list, lt.size(list)-num+1, num)

    for job in lt.iterator(jobs1):
        table1.append([job['title'],
        job['company_name'],
        job['experience_level'],
        job['published_at'],
        job['country_code'],
        job['city']])

    for job in lt.iterator(jobs2):
        table2.append([job['title'],
        job['company_name'],
        job['experience_level'],
        job['published_at'],
        job['country_code'],
        job['city']])
        
    return table1, table2

# IMPRIMIR RESULTADOS DE ANALISIS - TIEMPO Y MEMORIA
def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")
        
def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', True):
        return True
    else:
        return False

# Se crea el controlador asociado a la vista
control = new_controller()
# Variables utiles para el programa
SizeOpStr = """Seleccione el tamaño de CSV a cargar:
                 1. 10-por ||
                 2. 20-por ||
                 3. 30-por ||
                 4. 40-por ||
                 5. 50-por ||
                 6. 60-por ||
                 7. 70-por ||
                 8. 80-por ||
                 9. 90-por ||
                 10. small ||
                 11. medium||
                 12. large ||
                 """     
# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1: # CARGA DE DATOS ------------------------------------------------------
            print("Cargando información de los archivos ....\n")
            # Definir que archivos csv se van a utilizar para cargar datos -------------------------
            print("Que datos desea cargar?\n")
            SizeOp = input(SizeOpStr)
            SizeOp = int(SizeOp)
            Sizemsg, DataSize = controller.set_data_size(SizeOp)      
            controller.Route = DataSize    
            print(Sizemsg) 
            # Observar uso de memoria en la carga de datos ----------------------------------------
            print("Desea observar el uso de memoria? (True/False)")
            mem = input("Respuesta: ")
            mem = castBoolean(mem)
            # Ejecutar comando de cargar datos
            ans = load_data(control, memflag=mem)
            printLoadDataAnswer(ans)
            # Cantidad de datos guardados ---------------------------------------------------------
            print('Ofertas cargadas: ' + str(controller.set_data_size(control))) 
            #print('Libros cargados: ' + str(controller.skills_size(control))) 
            #print('Libros cargados: ' + str(controller.employment_size(control))) 
            #print('Libros cargados: ' + str(controller.multilocation_size(control))) 
            # Ofertas a visualizar
            num = input('Cuantas ofertas desea visualizar ')
            table1, table2 = printTableJobs(control["model"]["Trabajos"], int(num))
            print('Primeras ' + str(num) + " Ofertas")
            print(tabulate(table1))
            print('Ultimas ' + str(num) + " Ofertas")
            print(tabulate(table2))   
            
        elif int(inputs) == 2:
            print_req_1(control)
    
    
        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
