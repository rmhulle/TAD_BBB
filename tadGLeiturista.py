#!/usr/bin/python
# -*- coding:utf-8 -*-

""" Programa para teste parser

54 41 44 30 00 1C 00 00 00 00 AA 55 00 13 28 72 60 05 0A 02  00 00 0105 0A 07 FF FF FF 05 0A 0C FF FF FF 33 63 00 
54414430001C00000000AA550013287260050A02000001050A07FFFFFF050A0CFFFFFF336300 

54 41 44 - Cabeçalho "TAD"
30 - Versao 3.0 do sistema
00 - Byte livre
1C - RSSI - Qualidade do sinal em dBm
00 00 00 00 - Bytes livres
AA 55 - Preâmbulo do pacote PIMA agrupado (Sempre 2 bytes)
00 13 28 72 60 - Serial do Medidor (Sempre 5 bytes)
05 - Tamanho do consumo ativo + escopo e índice
0A 02 - Escopo e índice do KWh
00 00 01 - Consumo do KWh
05 - Tamanho do consumo Reativo Indutivo + Escopo e índice
0A 07 - Esopo e índice do Reativo Indutivo
FF FF FF - Consumo KWh do Reativo Indutivo - FF por não ter medidor!
05 - Tamanho do consumo capacitivo + escopo e índice
0A 0C - Escopo e índice do capacitivo
FF FF FF - Consumo KWh do Capacitivo - FF por não ter medidor!
33 63 - CRC
00 - BCC (!Inativo!) """

import serial
import time
import MySQLdb



medidor = 0
leiturista = 0




"""medidor = serial.Serial('/dev/ttyUSB0', 9600)
if ( medidor != 0 ):
	print("Serial Medidor OK")
else: 
	print("Serial Medidor Erro")"""	


leiturista = serial.Serial('/dev/ttyUSB1', 9600)

if ( leiturista != 0 ):
	print("Serial leiturista OK")
else: 
	print("Serial leiturista Erro")


con = MySQLdb.connect(host='localhost', user='root', passwd='zaruc',db='TAD')
c = con.cursor()

print("Banco De Dados OK")


while True:
	
	if leiturista.inWaiting()> 0:
		
			if (leiturista.readline(12)=="ATTAD_QTE\r\n"):
				number_rows = c.execute('SELECT * FROM leitura')
				
				print("foram encontrados %s ocorrencias" %number_rows)
				leiturista.write("QTE%s\r\n" %number_rows)
				index = 0

			elif ( leiturista.readline(12)=="FIM\r\n"):
				print("fim do envio")
			
			elif (leiturista.readline(12)=="ATTAD_REC0\r\n"):
				print("Linha %d" %index)
				rows = c.fetchone() 
				print rows[1]
				index = index + 1	
					 	
			

















"""c.execute("INSERT INTO `leitura` VALUES(30,223,21,23,24,CURRENT_TIMESTAMP)")"""
"""c.execute("INSERT INTO `leitura` VALUES(ID,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)"%(2,3,4,5,6,7))"""
"""c.execute('SELECT * FROM leitura WHERE serial=%s',(3))"""
"""c.execute("UPDATE `leitura` SET  `c_ativo` = %r WHERE  `leitura`.`serial` =%r"%(consumo_reativo,cdc))"""
"""c.execute('SELECT * FROM leitura WHERE serial=%r'%(cdc))"""
	



