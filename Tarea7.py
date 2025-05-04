import json
import requests
import os

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
            
 #Extraccion del fichero JSON de la web
file='https://raw.githubusercontent.com/openfootball/worldcup.json/refs/heads/master/2022/worldcup.groups.json'
 #Hacer la solicitud GET
response = requests.get(file)
 #Verificar si la solicitud fue exitosa
if response.status_code == 200: #respuesta exitosa
    data = response.json()  # Convertir el contenido a un diccionario de Python llamado data   
else: #Mostrar el código de error si no se puede acceder a la web con el archivo JSON
    print(f"Error al obtener el JSON. Código de estado: {response.status_code}")

ListaEquipos=[] #Lista de equipos participantes en el mundial para utilizar en programa leida del archivo web JSON
for i in data['groups']:
    for x in i['teams']:
        ListaEquipos.append(x)
while True: #bucle para el menú  
    print(f''' Seleccione una opción del menú:
        1)El número de equipos participantes en {data['name']}
        2)El número de grupos participantes en {data['name']}
        3)Introducir el equipo que fue a {data['name']}, en Inglés
        4)Salir''')
    op=ingresarnumero()
    match op:
        case 1: #Contamos el numero de equipos en la lista del JSON para saber cuantos participantes hubo
            print('El numero de equipos participantes en el torneo {} es: '.format(data['name']),len(ListaEquipos))
            fin()
        case 2: #Contamos el numero de grupos creando una nueva lista con el diccionario extraido del JSON
            print('El número de grupos del torneo {} es: '.format(data['name']),len(list((data['groups']))))
            fin()
        case 3:
            EquipoParticipante=str(input('Introduzca el equipo que crea que fue a {} (País en Inglés): '.format(data['name'])))
            EquipoParticipante=EquipoParticipante.capitalize() #Capitalizamos la primera letra del nombre del equipo
            if EquipoParticipante in ListaEquipos:
                print(EquipoParticipante,'estuvo en {}'.format(data['name']))
            else:
                print(EquipoParticipante,'NO fue a {}'.format(data['name']))
            fin()
        case 4:
            print('Gracias por utilizar nuestro programa')
            fin()
            break
        case _: #Excepcion del case para que no se introduzcan valores no listados
            print('No es un valor del menú, vuelva a intentarlo:')