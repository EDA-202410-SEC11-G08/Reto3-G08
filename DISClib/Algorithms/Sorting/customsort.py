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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from DISClib.ADT import list as lt
assert cf

"""
El algoritmo de ordenamiento que se implementa en este módulo puede ser:
    1) Tim Sort
    2) Patience Sort

    ######################## TIM SORT ########################

    El pseudocódigo para Tim Sort es:

        ------------------------------------------
        Function timSort(arr, n)
            min_run = 32
            For i = 0 to n step min_run
                insertionSort(arr, i, min(i+min_run-1, n-1))
            End For
            current_size = min_run
            While current_size < n
                For left = 0 to n step 2*current_size
                    mid = min(left + current_size - 1, n-1)
                    right = min(left + 2*current_size - 1, n-1)
                    merge(arr, left, mid, right)
                End For
                current_size = current_size * 2
            End While
        End Function
        ------------------------------------------

    El pseucodógido para la variante del algoritmo de ordenamiento por
    inserción es:

        ------------------------------------------
        Function insertion(arr, left, right)
            For i = left+1 to right
                j = i
                While j > left and arr[j] < arr[j-1]
                    swap(arr[j], arr[j-1])
                    j = j-1
                End While
            End For
        End Function
        ------------------------------------------

    El pseudocódigo para el algoritmo de ordenamiento por merge es:

        ------------------------------------------
        Function merge(arr, left, mid, right)
            len1 = m - l + 1
            len2 = r - m
            l = new Array(len1)
            r = new Array(len2)
            For i = 0 to len1
                l[i] = arr[l + i]
            End For
            For i = 0 to len2
                r[i] = arr[m + 1 + i]
            End For
            i = 0
            j = 0
            k = l
            While i < len1 and j < len2
                If l[i] <= r[j]
                    arr[k] = l[i]
                    i = i + 1
                Else
                    arr[k] = r[j]
                    j = j + 1
                End If
                k = k + 1
            End While
            While i < len1
                arr[k] = l[i]
                i = i + 1
                k = k + 1
            End While
            While j < len2
                arr[k] = r[j]
                j = j + 1
                k = k + 1
            End While
        End Function
        ------------------------------------------

    Para mayor información sobre Tim Sort, ver:
        - https://en.wikipedia.org/wiki/Timsort
        - https://www.geeksforgeeks.org/timsort/
        - https://www.youtube.com/watch?v=_dlzWEJoU7I



    ################# PATIENCE SORT #################

    El pseuocodigo para Patience Sort es:
        ------------------------------------------
        Function patienceSort(arr, n)
            piles = 0
            top = new Array(n)
            for i = 0 to n
                left = 0
                right = piles
                while left < right
                    mid = (left + right)/2
                    if arr[i] > top[mid]
                        left = mid + 1
                    else
                        right = mid
                    end if
                end while
                if left == piles
                    piles = piles + 1
                end if
                top[left] = arr[i]
            end for
            return piles
        End Function
        ------------------------------------------

    Para mayor información sobre Patience Sort, ver:
        - https://en.wikipedia.org/wiki/Patience_sort
        - https://www.geeksforgeeks.org/patience-sort/
        - https://www.youtube.com/watch?v=K9M6g7BiBX4

"""


def sort(lst, sort_crit):
    """sort ordena una lista de elementos utilizando el algoritmo
    implementado por el usuario. puede ser Tim Sort o Patient Sort.

    Args:
        lst (list): La lista a ordenar.
        sort_crit (func): Es una función definida por el usuario que
        representa el criterio de ordenamiento.

    Returns:
        list: La lista ordenada.
    """
    # TODO implementar el algoritmo de ordenamiento seleccionado lab 5
    # TODO cree todas las funciones y variables auxiliares que necesite
    n = lt.size(lst) 
    return timSort(lst, n, sort_crit)
    
def timSort(lst, n, sort_crit):
    min_run = setMinRun(n)
    for i in range(1, n+1, min_run):
        insertion(lst,sort_crit, i, min(i+min_run-1, n))
    current_size = min_run
    while (current_size <= n):
        for left in range(1, n+1, 2*current_size):
            mid = min(left + current_size - 1, n)
            right = min(left + 2*current_size - 1, n)
            if (mid < right):
                merge(lst,sort_crit, left, mid, right)
        current_size = current_size * 2
        
    return lst
# ===========================================
# Funciones auxiliares para Tim Sort
# ===========================================

# Rango mínimo del recorrido para el algoritmo Tim Sort
MIN_MERGE = 32


def setMinRun(n):
    """setMinRun calcula el recorrido minimo entre 23 y 64 para que la
    relación len(lst)/min_run sea igual o menor a una potencia de 2.

    Args:
        n (int): El tamaño de la lista a ordenar.

    Returns:
        int: El tamaño mínimo de la corrida.
    """
    R = 0
    while n >= MIN_MERGE:
        R |= n & 1
        n >>= 1
    min_run = n + R
    return min_run


def insertion(lst, sort_crit, left_idx, right_idx):
    """insertion ordena una lista de elementos utilizando con una variante
    del algoritmo de inserción entre los indices izquierdo (left_idx) y
    derecho (right_idx) con un recorrido de a lo sumo min_run.

    Args:
        lst (list): La lista a ordenar.
        sort_crit (func): Es una función definida por el usuario para
        comparar los elementos de la lista.
        left_idx (int): El índice izquierdo de la lista.
        right_idx (int): El índice derecho de la lista.

    Returns:
        list: La lista ordenada.
    """
    # TODO implementar la parte del insertion para el timsort en el lab 5
    for i in range(left_idx+1, right_idx+1):
        j = i
        while (j > left_idx) and sort_crit(lt.getElement(lst, j), lt.getElement(lst, j-1)):
            lt.exchange(lst, j, j-1)
            j = j-1
    return lst

    
def merge(lst, sort_crit, left_idx, mid_idx, right_idx):

    """merge fusiona los recorridos previamente ordenados con el insertion.

    Args:
        lst (list): La lista a ordenar.
        sort_crit (func): Es una función definida por el usuario para
        comparar los elementos de la lista.
        left_idx (int): El índice izquierdo de la lista.
        mid_idx (int): El índice medio de la lista.
        right_idx (int): El índice derecho de la lista.

    Returns:
        list: La lista ordenada.
    """
    len1 = mid_idx - left_idx + 1
    len2 = right_idx - mid_idx
    l = lt.newList("ARRAY_LIST") #Len1
    r = lt.newList("ARRAY_LIST") #Len2
    for i in range(1, len1+1):
        lt.addLast(l, lt.getElement(lst, left_idx + (i-1)))
    for i in range(1, len2+1):
        lt.addLast(r, lt.getElement(lst, mid_idx + 1 + (i-1)))
    i = 1
    j = 1
    k = left_idx
    
    while (i <= len1) and (j <= len2):
        if sort_crit(lt.getElement(l,i), lt.getElement(r, j)):
            lt.changeInfo(lst, k, lt.getElement(l,i))
            i = i + 1
        else:
            lt.changeInfo(lst, k, lt.getElement(r,j))
            j = j + 1
        k = k + 1
        
    while (i <= len1):
        lt.changeInfo(lst, k, lt.getElement(l,i))
        i = i + 1
        k = k + 1
        
    while (j <= len2):
        lt.changeInfo(lst, k, lt.getElement(r,j))
        j = j + 1
        k = k + 1
    return lst
# ===========================================
# Funciones auxiliares para Patience Sort
# ===========================================


def merge_pile(pile_lt, sort_crit):
    """merge_pile resive una lista de pilas y las fusiona en una sola lista
    ordenada.

    Args:
        pile_lt (list): lista de pilas a fusionar.
        sort_crit (func): Es una función definida por el usuario que
        representa el criterio de ordenamiento.

    Returns:
        list: lista ordenada.
    """
    # TODO implementar la parte del merge para el patience sort en el lab 5
    pass
