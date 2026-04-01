"""Type, Comprensión de Listas, Sorted y Filter."""

from typing import List, Union


def numeros_al_final_basico(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Toma una lista de enteros y strings y devuelve una lista con todos los
    elementos numéricos al final.
    """
    pass # Completar
    no_numeros = []
    numeros = []
    for elemento in lista:
        if isinstance(elemento, (int, float)):
            numeros.append(elemento)
        else:
            no_numeros.append(elemento)
    return no_numeros + numeros


# NO MODIFICAR - INICIO
assert numeros_al_final_basico([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_comprension(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando comprensión de listas."""
    pass # Completar
    no_numeros = [x for x in lista if not isinstance(x, (int, float))]
    numeros = [x for x in lista if isinstance(x, (int, float))]
    return no_numeros + numeros


# NO MODIFICAR - INICIO
assert numeros_al_final_comprension([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_sorted(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """Re-escribir utilizando la función sorted con una custom key.
    Referencia: https://docs.python.org/3/library/functions.html#sorted
    """
    pass # Completar
    return sorted(lista, key=lambda x: isinstance(x, (int, float)))


# NO MODIFICAR - INICIO
assert numeros_al_final_sorted([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


def numeros_al_final_filter(lista: List[Union[float, str]]) -> List[Union[float, str]]:
    """CHALLENGE OPCIONAL - Re-escribir utilizando la función filter.
    Referencia: https://docs.python.org/3/library/functions.html#filter
    """
    pass # Completar
    no_numeros = list(filter(lambda x: not isinstance(x, (int, float)), lista))
    numeros = list(filter(lambda x: isinstance(x, (int, float)), lista))
    return no_numeros + numeros


# NO MODIFICAR - INICIO
if __name__ == "__main__":
    assert numeros_al_final_filter([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN


###############################################################################


#def numeros_al_final_recursivo(lista: List[Union[float, str]]) -> List[Union[float, str]]:
 #   """CHALLENGE OPCIONAL - Re-escribir de forma recursiva."""
  #  if not lista:
   #     return []

   # primero = lista[0]
   # resto = numeros_al_final_recursivo(lista[1:])

   # if isinstance(primero, str):
   #     return [primero] + resto
   # else:
   #     return resto + [primero]


# NO MODIFICAR - INICIO
#if __name__ == "__main__":
 #   assert numeros_al_final_recursivo([3, "a", 1, "b", 10, "j"]) == ["a", "b", "j", 3, 1, 10]
# NO MODIFICAR - FIN
