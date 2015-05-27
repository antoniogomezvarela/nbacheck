# -*- coding: utf-8 -*-
from bottle import default_app, route, run, get, post, template, request, static_file, debug
import time
import datetime
import requests
import json
from xml.etree import ElementTree

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@route('/')
def index():
	return template('index')

@route('/este')
def este():
	clasificacioneste= []
	ganadoseste = []
	perdidoseste = []
	favoreste = []
	contraeste = []
	diferenciaeste = []
	teamideste=[]
	contador=1
	headers=""

	diccmes={'January':'01','February':'02','March':'03','April':'04','May':'05',
			'June':'06','July':'07','August':'08','September':'09','October':'10',
			'November':'11','December':'12'}
	anno = datetime.date.today().strftime("%Y")
	mesactual = datetime.date.today().strftime("%B")
	dia = datetime.date.today().strftime("%d")

	mes=diccmes[mesactual]

	#cabecera
	headers={"content-type":"text","User-Agent":"antoniomgomez/antoniomgomezvarela@gmail.com",
			"Authorization": "Bearer 405385ac-b894-4d56-a5cc-9be1bafe4cd2"}

	req = requests.get("https://erikberg.com/nba/standings/%s%s%s.json"% (anno,mes,dia), headers=headers)
	salida = json.loads(req.text)

	for i in salida['standing']:
		if i['conference']=="EAST":
			first_name = i['first_name']
			ganados= i['won']
			perdidos = i['lost']
			favor = i['points_for']
			contra= i['points_against']
			diferencia= i['point_differential']
			team_id= i['team_id']
			#team_id=team_id.replace("-","_")
			clasificacioneste.append(first_name)
			ganadoseste.append(ganados)
			perdidoseste.append(perdidos)
			favoreste.append(favor)
			contraeste.append(contra)
			diferenciaeste.append(diferencia)
			teamideste.append(team_id)

	return template('este', clasificacioneste=clasificacioneste, 
		ideste=teamideste, ganadoseste=ganadoseste, perdidoseste=perdidoseste,
		favoreste=favoreste, contraeste=contraeste, diferenciaeste=diferenciaeste)


@route('/oeste')
def oeste():
	clasificacionoeste= []
	ganadosoeste = []
	perdidosoeste = []
	favoroeste = []
	contraoeste = []
	diferenciaoeste = []
	teamidoeste=[]
	contador=1
	headers=""

	diccmes={'January':'01','February':'02','March':'03','April':'04','May':'05',
			'June':'06','July':'07','August':'08','September':'09','October':'10',
			'November':'11','December':'12'}
	anno = datetime.date.today().strftime("%Y")
	mesactual = datetime.date.today().strftime("%B")
	dia = datetime.date.today().strftime("%d")

	mes=diccmes[mesactual]

	#cabecera
	headers={"content-type":"text","User-Agent":"antoniomgomez/antoniomgomezvarela@gmail.com",
			"Authorization": "Bearer 405385ac-b894-4d56-a5cc-9be1bafe4cd2"}

	req = requests.get("https://erikberg.com/nba/standings/%s%s%s.json"% (anno,mes,dia), headers=headers)
	salida = json.loads(req.text)

	for i in salida['standing']:
		if i['conference']=="WEST":
			if i['last_name']=="Clippers":
				first_name = "L.A. Clippers"
			elif i['last_name']=="Lakers":
				first_name = "L.A. Lakers"
			first_name=i['first_name']
			ganados= i['won']
			perdidos = i['lost']
			favor = i['points_for']
			contra= i['points_against']
			diferencia= i['point_differential']
			team_id = i['team_id']
			#team_id=team_id.replace("-","_")
			clasificacionoeste.append(first_name)
			ganadosoeste.append(ganados)
			perdidosoeste.append(perdidos)
			favoroeste.append(favor)
			contraoeste.append(contra)
			diferenciaoeste.append(diferencia)
			teamidoeste.append(team_id)

	return template('oeste', clasificacionoeste=clasificacionoeste, 
		idoeste=teamidoeste, ganadosoeste=ganadosoeste, perdidosoeste=perdidosoeste,
		favoroeste=favoroeste, contraoeste=contraoeste, diferenciaoeste=diferenciaoeste)

@get('/equipo')
def equipo():
	idequipo = request.GET.get('idequipo').strip()
	
	#cabecera
	headers={"content-type":"text","User-Agent":"antoniomgomez/antoniomgomezvarela@gmail.com",
			"Authorization": "Bearer 405385ac-b894-4d56-a5cc-9be1bafe4cd2"}
	
	#Jugadores
	listajugadores = []
	listaposiciones = []
	listaaltura = []
	listapeso = []
	listaedad = []

	req = requests.get("https://erikberg.com/nba/roster/%s.json"% idequipo, headers=headers)
	salida = json.loads(req.text)

	equipo = salida['team']['full_name']

	for i in salida['players']:
		jugadores = i['display_name']
		posiciones = i['position']
		altura = i['height_cm']
		peso = i['weight_kg']
		edad = i['age']
		listajugadores.append(jugadores)
		listaposiciones.append(posiciones)
		listaaltura.append(altura)
		listapeso.append(peso)
		listaedad.append(edad)

	#Partidos
	listaidpartido=[]
	listaoponente=[]
	listapfavor=[]
	listapcontra=[]

	anno = datetime.date.today().strftime("%Y")

	req = requests.get("https://erikberg.com/nba/results/%s.json?season=%s"% (idequipo,anno), headers=headers)
	salida = json.loads(req.text)

	for i in salida:
		idpartido=i['event_id']
		oponente=i['opponent']['full_name']
		pfavor=i['team_points_scored']
		pcontra=i['opponent_points_scored']
		listaidpartido.append(idpartido)
		listaoponente.append(oponente)
		listapfavor.append(pfavor)
		listapcontra.append(pcontra)

	idequipo=idequipo.title()
	wikiequipo=idequipo.replace("-","_")
	req = requests.get("https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&exintro=&explaintext=&titles=%s"% wikiequipo)
	tree = ElementTree.fromstring(req.content)
	descrip=tree[0][1][0][0].text

	return template('equipo',equipo=equipo ,listajugadores=listajugadores, 
					listaposiciones=listaposiciones, listaaltura=listaaltura,
					listapeso=listapeso, listaedad=listaedad,listaoponente=listaoponente, 
					listapfavor=listapfavor,listapcontra=listapcontra, 
					listaidpartido=listaidpartido,descrip=descrip)

@get('/partido')
def partido():
	idpartido = request.GET.get('idpartido').strip()
		
	#cabecera
	headers={"content-type":"text","User-Agent":"antoniomgomez/antoniomgomezvarela@gmail.com",
			"Authorization": "Bearer 405385ac-b894-4d56-a5cc-9be1bafe4cd2"}

	req = requests.get("https://erikberg.com/nba/boxscore/%s.json"% idpartido, headers=headers)
	salida = json.loads(req.text)

	visitante=salida['away_team']['full_name']
	local=salida['home_team']['full_name']
	cuartoslocal=salida['home_period_scores']
	cuartosvisitante=salida['away_period_scores']

	listaljugador=[]
	listalpos=[]
	listalpuntos=[]
	listalasis=[]
	listalperdidas=[]
	listalrobos=[]
	listalfaltas=[]
	listavjugador=[]
	listavpos=[]
	listavpuntos=[]
	listavasis=[]
	listavperdidas=[]
	listavrobos=[]
	listavfaltas=[]

	for i in salida['away_stats']:
		nombre = i['display_name'] 
		posicion = i['position']
		puntos = i['points']
		asistencias = i['assists']
		perdidas = i['turnovers']
		robos = i['steals']
		faltas = i['personal_fouls']
		listavjugador.append(nombre)
		listavpos.append(posicion)
		listavpuntos.append(puntos)
		listavasis.append(asistencias)
		listavperdidas.append(perdidas)
		listavrobos.append(robos)
		listavfaltas.append(faltas)

	for x in salida['home_stats']:
		nombre = x['display_name'] 
		posicion = x['position']
		puntos = x['points']
		asistencias = x['assists']
		perdidas = x['turnovers']
		robos = x['steals']
		faltas = x['personal_fouls']
		listaljugador.append(nombre)
		listalpos.append(posicion)
		listalpuntos.append(puntos)
		listalasis.append(asistencias)
		listalperdidas.append(perdidas)
		listalrobos.append(robos)
		listalfaltas.append(faltas)

	return template('partido', visitante=visitante,local=local,cuartosvisitante=cuartosvisitante,cuartoslocal=cuartoslocal,
					listavjugador=listavjugador,listavpos=listavpos,listavpuntos=listavpuntos,listavasis=listavasis,
					listavperdidas=listavperdidas,listavrobos=listavrobos,listavfaltas=listavfaltas,listaljugador=listaljugador,
					listalpos=listalpos,listalpuntos=listalpuntos,listalasis=listalasis,listalperdidas=listalperdidas,
					listalrobos=listalrobos,listalfaltas=listalfaltas)


# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/')) 

application=default_app()