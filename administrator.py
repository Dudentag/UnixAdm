
#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Dudentag'
"""
Copyright: Manolo
Licencia: Affero GPL V3
Requisitos: Python 2.4 Si se quiere usar el modulo Subprocess en lugar de os
Si se ejecuta en python 3.x se debe cambiar la llamada "raw_input" por "input"

Script para monitorizar sistemas.

Uso:
----
Ejecute en una linea de comandos:

$ python monitoriza.py -h

"""

import commands
import os
import sys
#import subprocess
import getopt

#######################################
##Definicion de las funciones empleadas
#######################################
def ImpSalida():
	#Imprime por pantalla el fichero de salida
	f = open("/tmp/monitoriza_temp", "r")
	while True:
		linea = f.readline()
		if not linea: break
		print linea
	f.close()


def MandaMailParam():
	#Manda el mail solicitando los parametros de envio
	f = open("/tmp/monitoriza_temp", "r")
	mssg = f.read()
	f.close()
	SENDMAIL = "/usr/sbin/sendmail"
	p = os.popen("%s -t" % SENDMAIL, "w")
	mail = raw_input("Indique el mail de destino:")
	asunto = raw_input("Indique el asunto del mail:")
	p.write("To: "+mail+"\n")
	p.write("Subject: "+asunto+"\n")
	p.write("\n")
	p.write(mssg)
	sts = p.close()


def MandaMail():
	# Obtiene el texto de la Monitorizacion
	f = open("/tmp/monitoriza_temp", "r")
	mssg = f.read()
	f.close()
	#Genera y manda el mail
	SENDMAIL = "/usr/sbin/sendmail"
	p = os.popen("%s -t" % SENDMAIL, "w")
	p.write("To: XXXX@XXXX.com\n")
	p.write("Subject: Monitorizacion\n")
	p.write("\n")
	p.write(mssg)
	sts = p.close()



#Obtiene la Swap libre y la ocupada y determina si se esta usando o no mas del 50%
def ObtConSwap():
	result1=commands.getoutput('cat /proc/meminfo|grep "SwapTotal:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	result2=commands.getoutput('cat /proc/meminfo|grep "SwapFree:"|tr -s "'" "'"|cut -d "'" "'" -f 2')
	##mem.ocupada=mem.total-mem.libre
	result3=int(result1)-int(result2)
	##Si la mem.ocupada es mayor que la mem.total/2
	if int(result3)>int(result1)/2:
		cont=0
	else:
		cont=1
	return cont


#Devuelve 1 si encuentra un valor superior a 90 sino devuelve 0
#Al final del comando con sed eliminamos el ultimo caracter que era un '%' por ''
def ObtOcuPart():
	cont=0
	result=commands.getoutput('df -h|tr -s "'" "'"|cut -d "'" "'" -f 5|grep %|sed -e "'"1d"'"|sed "'"s/.$//g"'"')
	ruta="/tmp/monitoriza_temp2"
	wfich(str(result),ruta)
	f=open(ruta,"r")
	for linea in f.readlines():
		if linea[:-1]!="":
			if int(linea[:-1])>90:
				cont=1
	return cont

#Obtiene la media tiempo ocioso de la CPU para 10 iteraciones
#Con sed eliminamos las 2 primeras lineas
def ObtConCPU():
	iter=10
	result=commands.getoutput('vmstat 5 '+str(iter)+'|sed -e "'"1,2d"'"|tr -s "'" "'"|cut -d "'" "'" -f 16')
	ruta="/tmp/monitoriza_temp2"
	wfich(str(result),ruta)
	f=open(ruta,"r")
	s=0
	for linea in f.readlines():
		if linea!="":
			s=int(s)+int(linea)
	result1=int(s)/int(iter)
	f.close()
	commands.getoutput('rm -f'+ruta)
	return result1

#Obtiene el numero de interfaces con errores
def ObtEstInterfaces():
	result=commands.getoutput('/sbin/ifconfig -a|grep errors|tr -s "'" "'"|cut -d "'" "'" -f 4|grep -v errors:0|wc -l')
	return result

#Obtiene el numero de interfaces con colisiones
def ObtEstInterfaces2():
	result=commands.getoutput('/sbin/ifconfig -a|grep collisions|tr -s "'" "'"|cut -d "'" "'" -f 2|grep -v collisions:0|wc -l')
	return result

#Obtiene el nombre de la maquina
def ObtNom():
	result=commands.getoutput('uname -a')
	return result

#Obtiene la fecha y hora de la maquina
def ObtFecha():
	result=commands.getoutput('date')
	return result

#Obtiene el % de memoria usada
def checkmem():
	result1 = commands.getoutput('free|grep Mem:|tr -s "'" "'" |cut -d "'" "'" -f 2')
	result2 = commands.getoutput('free|grep Mem:|tr -s "'" "'" |cut -d "'" "'" -f 3')
	result3=int(result2)*100/int(result1)
	return result3

#Escribe machacando el contenido en un fichero
def wfich(linea,fichero):
	fich_maquinas=open(fichero, "w")
	fich_maquinas.write(linea)
	fich_maquinas.close()

#Escribe anyadiendo el contenido al final de en un fichero
def afich(linea,fichero):
	fich_maquinas=open(fichero, "a")
	fich_maquinas.write(linea)
	fich_maquinas.close()

def Monitor():
	#Ruta del fichero temporal a generar con los resultados de la monitorizacion
	ruta1="/tmp/monitoriza_temp"

	#Escribe a fichero la fecha de la monitorizacion, iniciando el fichero, creandolo o machacandolo
	fech=ObtFecha()
	fech1=str(fech)+'\n\n'
	wfich(str(fech1),ruta1)

	#Escribe a fichero el nombre de la maquina, iniciando el fichero para anyadir al final
	nom=ObtNom()
	nom1=str(nom)+'\n\n'
	afich(str(nom1),ruta1)

	#Si el consumo de memoria RAM es superior al 85% escribe un aviso si es menor otro
	mem=checkmem()
	if int(mem)>85:
		afich('ERROR - Ocupacion de memoria ELEVADA ->'+str(mem)+'%\n\n',ruta1)
	else:
		afich('OK - Ocupacion de memoria Correcta ->'+str(mem)+'%\n\n',ruta1)


	#Si el numero de interfaces con errores es superior a 0 escribe un aviso si es =0 escribe otro
	inter=ObtEstInterfaces()
	if int(inter)>0:
		afich('ERROR - Existen errores en algunas interfaces\n\n',ruta1)
	else:
		afich('OK - Todas las interfaces sin errores\n\n',ruta1)

	#Si el numero de interfaces con colisiones es superior a 0 escribe un aviso si es =0 escribe otro
	inter=ObtEstInterfaces2()
	if int(inter)>0:
		afich('ERROR - Existen colisiones en algunas interfaces\n\n',ruta1)
	else:
		afich('OK - Todas las interfaces sin colisiones\n\n',ruta1)

	#Si el consumo de CPU es mayor de 75 escribe un aviso si no lo da como correcto
	id=ObtConCPU()
	if int(id)<75:
		afich('ERROR - El consumo de CPU es demasiado elevado ->'+str(id)+'% id\n\n',ruta1)
	else:
		afich('OK - El consumo de CPU es correcto ->'+str(id)+'% id\n\n',ruta1)

	#Si la ocupacion de una particion supera el 90% deja un aviso sino lo da como correcto
	part=ObtOcuPart()
	if int(part)==1:
		afich('ERROR - Hay particiones con una ocupacion mayor al 90%\n\n',ruta1)
	else:
		if int(part)==0:
			afich('OK - Ocupacion de las particiones correcta\n\n',ruta1)
		else:
			afich('Error al monitotizar las particiones\n\n',ruta1)

	#Determina si se esta usando mas del 50% de la Swap
	sw=ObtConSwap()
	if sw==0:
		afich('ERROR - Mas del 50% de la Swap esta siendo usada\n\n',ruta1)
	else:
		if sw==1:
			afich('OK - El uso de la Swap es correcto menor al 50%\n\n',ruta1)
		else:
			afich('Error al monitotizar la Swap\n\n',ruta1)


#Lanza un print's especificando los parametros aceptados.
def Uso():
	print "Los parametros permitos son los siguientes:"
	print ""
	print "1: '-h' '--help' --> Muestra los parametros permitidos"
	print "2: '-m' '--mail' --> Monitoriza el sistema y manda el resumen por correo"
	print "3: '-s' '--screen' --> Monitoriza el sistema y muestra el resumen por pantalla"
	print "3: '-x' '--mailcarta' --> Monitoriza el sistema y manda el resumen por correo solicitando los parametros de envio"


#
def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hg:d,m,s,x", ["help", "mail", "screen","mailcarta"])
	except getopt.GetoptError:
		Uso()
		sys.exit()
	print "Use '-h' para ver los parametros aceptados"
	print ""
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			Uso()
			sys.exit()
		elif opt in ("-s", "--screen"):
			print "Screen"
			Monitor()
			ImpSalida()
		elif opt in ("-m", "--mail"):
			print "Mail"
			Monitor()
			MandaMail()
		elif opt in ("-x", "--mailcarta"):
			print "MailCarta"
			Monitor()
			MandaMailParam()

#Llamamos a Main pasandole la lista de parametros, obiando el primero que es el
#nombre del script.
main(sys.argv[1:])