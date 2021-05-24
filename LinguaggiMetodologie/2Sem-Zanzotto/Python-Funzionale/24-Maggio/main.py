# uso la funzione sorted(), e come chiave del sorting uso
# una lambda che estrapola il secondo carattere della stringa

print(sorted("This is af test string".split(), key=lambda x: x[1]))


# ------------------------------------------------------------------


# creo la nostra funzione map ( List, f() )
# che applica la funzione f a ogni elemento della lista

def my_map(list, function):
    new_list = []
    for i in list:
        new_list.append(function(i))
    return new_list


print(my_map([1, 2, 3], lambda x: x * x))


# -------------------------------------------------------

def my_reduce(list, function):
    result = list[0]
    for i in range(1, len(list)):
        result = function(result, list[i])
    return result

print (my_reduce([1 , 3, 5, 6, 2, ], lambda a, b: a + b))
