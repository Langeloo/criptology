#key Schedduling Algoritm
def ksa(key, diccionario): 
    """
    Se inicializa el vextor S con el tamaño del vector 0 - 31
    Se inicia J en 0
    tClave obtiene el tamanno de la clave
    Se recorren todas las posiciones de S
    se itera y aplica formula KSA para vetcor J
    Se intercambias valores S[i] y S[j] para qie S sea aletaorio
    ord obtine el ASCII de un caracte
    """
    S = list(range(len(diccionario)))
    j = 0

    tClave = len(key)
    for i in range(len(diccionario)):
        j = (j + S[i] + ord(key[i % tClave])) % len(diccionario)
        S[i], S[j] = S[j], S[i]

    return S

#Pseudo-Random Generation Algoritm
def prga(S, diccionario):
    """
    Se ejecuta un bucle hasta alcnazar la longitud del diccionario
    Actualiza i (i accede a los elementos de S)
    Intercambia los valores de S[i] y S[j] nuevamente (permutacion)
    t selecciona un byte del diccionario pero tenendo en cuenta el rango(no se sale del rango)
    Se obtiene el valor de t en S y se agrega a K
    K se encaarga de la operacion XOR
    """
    i = j = k = 0
    key_stream = []

    while k < len(diccionario):
        i = (i + 1) % len(diccionario)
        j = (j + S[i]) % len(diccionario)
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % len(diccionario)
        key_byte = S[t]
        key_stream.append(key_byte)
        k += 1

    return key_stream

def rc4(key, mensaje, diccionario):
    """
    Se asegura que la longitud de K sea igual al mensaje original
    XOR entre K y el mensaje origianl
    format para convertir cada byte de K en una cadena binaria de 8 bits
    format para convertir cada byte del mensaje cifrado en una cadena binaria de 5 bits
    Se unen los bytes del menasje en una sola cadena
    """
    S = ksa(key, diccionario)
    key_stream = prga(S, diccionario)

    key_stream = key_stream[:len(mensaje)]

    m_encriptado = [diccionario[(diccionario.index(mensaje[i]) ^ key_stream[i]) % len(diccionario)]
    for i in range(len(key_stream))]

    key_stream_binario = ''.join(format(byte, '08b')
     for byte in key_stream)

    mc_binario = ''.join(format(diccionario.index(char), '05b')
     for char in m_encriptado)

    return key_stream_binario, mc_binario, ''.join(m_encriptado)

# ----------PRUEBA 32 CARACTERES---------------
diccionario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ12345"
mensaje = "MENSAJEDEPRUEBARC4PARACRIPTOLOGIA"
key = "CLAVE123"
# -------------------------------------------
# #----------PRUEBA 33 CARACTERES---------------
# diccionario = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ123456"
# mensaje = "MENSAJEDEPRUEBARC4PARACRIPTOLOGIA"
# key = "CLAVE1234"
# #-------------------------------------------

key_stream, m_codificado, m_encriptado = rc4(key, mensaje, diccionario)


print("Mensaje Original:", mensaje, "=>", len(mensaje),"caracteres")
print("Clave:", key)
print("")
print("KeyStream en binario:", key_stream, "=>", len(key_stream),"bits")
print("")
print("Codificacion en binario de 5 bits por caracter:", m_codificado, "=>",len(m_codificado),"bits")
print("")
print("Mensaje Cifrado en el diccionario:", m_encriptado, "=>",  len(m_encriptado),"caracteres")


#Ataque de fuerza bruta para una clave d 4 caracteres
ARRAY = "EAOLSNDRUITCPMYQ"
def fuerza_bruta(ARRAY, key, mensaje):
    """
    Se crea un diccionario con todas las posibles combinaciones de 4 caracteres
    Se recorre el diccionario y se aplica el algoritmo RC4
    Se compara el mensaje cifrado con el mensaje original
    Se imprime la clave que descifra el mensaje
    """
    initial_key_stream, initial_m_codificado, initial_m_encriptado = rc4(key, mensaje, ARRAY)
    print("Ataque de fuerza bruta")
    print("Diccionario:", ARRAY)
    print("Mensaje:", mensaje)
    print("Clave:", key)

    count = 0
    for i in range(len(ARRAY)):
        for j in range(len(ARRAY)):
            for k in range(len(ARRAY)):
                for l in range(len(ARRAY)):
                    key = ARRAY[i] + ARRAY[j] + ARRAY[k] + ARRAY[l]
                    count += 1
                    print(f"Probando clave: {count}. {key}")
                    key_stream, m_codificado, m_encriptado = rc4(key, mensaje, ARRAY)
                    if m_encriptado == initial_m_encriptado:
                        print("Clave encontrada:", key)
                        return
fuerza_bruta(diccionario, 'CAVE', mensaje)
