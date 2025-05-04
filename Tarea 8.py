import requests
import sqlite3
import pandas as pd
import os

headers = {"User-agent": 'Chrome/135.0.7049.85 Safari/537.36'}
url="https://es.wikipedia.org/wiki/Anexo:Sencillos_n%C3%BAmero_uno_en_Espa%C3%B1a#Canciones_con_m%C3%A1s_semanas_en_el_n%C3%BAmero_uno"
respuesta = requests.get(url,headers=headers)
all_tables = pd.read_html(respuesta.content)
matched_table = pd.read_html(respuesta.text)
# Guardar tabla en variable con nombre semántico
canciones = matched_table[1]
global dic
dic=canciones.to_dict(orient='index')


for i in dic: #Adecuacion de la lista para valores ambiguos
    if dic[i]['País']== 'Colombia Trinidad y Tobago':
        dic[i]['País']='Colombia'
    elif dic[i]['País']== 'Argentina España':
        dic[i]['País']='Argentina'
    if dic[i]['Año']=='1978/1991':
        dic[i]['Año']='1978'
def CrearInformacion(): # crea la informacion en el diccionario de continente segun pais
    for i in dic:
        Paises= dic[i]['País']
        if Paises == 'España' or Paises=='Reino Unido' or Paises=='Francia' or Paises=='Alemania' or Paises=='Suecia':
            dic[i]['Continente']='Europa'
        elif Paises == 'Estados Unidos' or Paises=='Canadá':
            dic[i]['Continente']='América del Norte'
        elif Paises== 'Venezuela' or Paises=='Puerto Rico' or Paises=='Colombia' or Paises=='Argentina' or Paises=='Cuba' or Paises=='Guyana' or Paises=='Brasil':
            dic[i]['Continente']='América del Sur'
    for j in dic: #Crea la informacion de diccionario de idioma según el País
        Paises= dic[j]['País']
        if Paises=='Estados unidos' or Paises=='Canadá' or Paises=='Reino Unido' or Paises=='Alemania' or Paises=='Suecia' or Paises=='Guyana':
            dic[j]['Idioma']='Inglés'
        elif Paises==('Brasil'):
            dic[j]['Idioma']='Portugués'
        elif Paises==('Francia'):
            dic[j]['Idioma']='Francés'
        else:
            dic[j]['Idioma']='Español'
    return None    
def ingresarnumero(): #Ingresa un numero y si no es un numero pide que se vuelva a ingresar
        try:
            r=int(input())
        except ValueError:
            print("No es un numero")
            r=ingresarnumero()
        return r
def fin(): #Pausa y limpieza de pantalla
    input('Pulse Intro para continuar')
    os.system('cls')
    return None         
def crearBD():#creacion de la base de datos
    conn=sqlite3.connect('BDCanciones.db')
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE if not exists TablaCanciones(
                ID integer primary key autoincrement,
                Posicion integer,
                Interprete varchar(100),
                Tema VARCHAR(100) unique,
                Año INTEGER,
                Semanas INTEGER,
                Pais varchar(29),
                Idioma varchar(29),
                Continente varchar(20))''') #creacion de la tabla con ID autoincremental y el campo Tema como unico
    try:
        for i in dic: #insercion de los datos en la tabla segun valores del diccionario global extraido de la tabla en la web
            cursor.execute("INSERT INTO TablaCanciones VALUES (null,?,?,?,?,?,?,?,?)",(dic[i]['N.º'],dic[i]['Intérprete'],dic[i]['Tema'],dic[i]['Año'],dic[i]['Semanas'],dic[i]['País'],dic[i]['Idioma'],dic[i]['Continente']))
    except sqlite3.IntegrityError: # excepcion para que no se inserten datos de nuevo en la tabla y produzca error con el campo unico 'Tema'
        print("El dato ya existe, no se insertó")
    conn.commit() 
    conn.close()
    return None
CrearInformacion()
crearBD()

while True: #bucle para el menú  
    #conexion con la base de datos
    conn=sqlite3.connect('BDCanciones.db')
    cursor=conn.cursor()
    #Menu de Opciones
    print(f''' Seleccione una opción del menú: 
        1)¿Cuales son las tres canciones con mas semanas en el numero uno?
        2)¿Cuántas canciones hay por idioma en la lista?
        3)¿Cuántas canciones son de América del Norte y cuántas de América del Sur?
        4)¿Cuál es el país con más canciones en la lista?
        5)¿Qué canciones son de Europa y están en un idioma diferente al inglés?
        6)¿Cuál es el promedio de semanas que las canciones han estado en el número uno, agrupadas por continente?
        7)¿Cuáles son las canciones más recientes (lanzadas después del año 2010) y cuántas hay por idioma?
        8)Salir del programa                   
          ''')
    op=ingresarnumero() #numero de opcion en el menu debe ser entero
    match op:
        case 1:
            print('¿cuales son las tres canciones con mas semanas en el numero uno?')
            cursor.execute("SELECT Tema, Semanas FROM TablaCanciones ORDER BY Semanas DESC LIMIT 3")
            resultados=cursor.fetchall()
            for i in resultados:
                print(f'{i[0]} con un total de {i[1]} semanas en el Nº1')
            fin()
        case 2:
            print('¿Cuántas canciones hay por idioma en la lista?')
            cursor.execute("SELECT Idioma, COUNT(*) FROM TablaCanciones GROUP BY Idioma")
            resultados=cursor.fetchall()
            for i in resultados:
                print(f'En {i[0]} hay un total de {i[1]} canciones')
            fin()
        case 3:
            print('¿Cuántas canciones son de América del Norte y cuántas de América del Sur?')
            cursor.execute('SELECT Continente, COUNT(*) FROM TablaCanciones where Continente In ("América del Norte","América del Sur") group by continente')
            resultados=cursor.fetchall()
            for i in resultados:
                print(f'De {i[0]} son un total de {i[1]} canciones')
            fin()
        case 4:
            print('¿Cuál es el país con más canciones en la lista?')
            cursor.execute('SELECT Pais, COUNT(*) FROM TablaCanciones GROUP BY Pais ORDER BY COUNT(*) DESC LIMIT 1')
            resultados=cursor.fetchone()            
            print('El país con más canciones en la lista es:\n{} con un total de {}'.format(resultados[0],resultados[1]))
            fin()
        case 5:
            print('¿Qué canciones son de Europa y están en un idioma diferente al inglés?')
            cursor.execute('SELECT Tema, Idioma, interprete from TablaCanciones WHERE Continente="Europa" AND Idioma is not "Inglés"')
            resultados=cursor.fetchall()
            for i in resultados:
                print(f'{i[0]} de {i[2]} cantada en {i[1]}')
            fin()
        case 6:
            print('¿Cuál es el promedio de semanas que las canciones han estado en el número uno, agrupadas por continente?')
            cursor.execute('SELECT continente, sum(Semanas)/count(Tema) from TablaCanciones group by continente')
            resultados=cursor.fetchall()
            for i in resultados:
                print('La media de un tema de {} es de {} semanas en el Nº1'.format(i[0],i[1]))
            fin()
        case 7:
            print('¿Cuáles son las canciones más recientes (lanzadas después del año 2010)?')
            cursor.execute('SELECT Tema, año from TablaCanciones where año>2010 order by Año asc')
            resultados=cursor.fetchall()
            for i in resultados:
                print(f'{i[0]} del año {i[1]}')
            print('¿Cuántas hay por idioma?')
            cursor.execute('SELECT count(idioma), idioma from TablaCanciones where año>2010 group by idioma')
            resultados=cursor.fetchall()
            for i in resultados:
                if i[0]<2:
                    print(f'{i[0]} es cantada en {i[1]}')
                else:
                    print(f'{i[0]} son cantadas en {i[1]}')
            fin()
        case 8: #Salida del programa
            print('Gracias por utilizar nuestro programa')
            conn.commit()
            conn.close()
            break
        case _: #Excepcion del case para que no se introduzcan valores no listados
            print('No es un valor del menú, vuelva a intentarlo:')
