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







medidor = serial.Serial('/dev/ttyUSB0', 9600)
print("Serial medidor")
con = MySQLdb.connect(host='localhost', user='root', passwd='zaruc',db='TAD')
c = con.cursor()
print("Banco De Dados concectado")

while True:
	
	if medidor.inWaiting()> 0:
			primeira = medidor.read(1)
			if (primeira=="T"):
				if (medidor.read(1)=="A"):
					if medidor.read(1)=="D":
						versao = medidor.read(1)
						byte_livre_1 = medidor.read(1)
						rssi = medidor.read(1)
						byte_livre_2 = medidor.read(4)
						preambulo = medidor.read(2)
						cdc = medidor.read(5)
						tam_ativo = medidor.read(1)
						escopo_ativo = medidor.read(2)
						consumo_ativo = medidor.read(ord(tam_ativo) - 2)
						tam_reativo = medidor.read(1)
						escopo_reativo = medidor.read(2)
						consumo_reativo = medidor.read(ord(tam_reativo) - 2)
						tam_capacitivo = medidor.read(1)
						escopo_capacitivo = medidor.read(2)
						consumo_capacitivo = medidor.read(ord(tam_capacitivo) - 2)
						crc = medidor.read(2)
						if (c.execute('SELECT * FROM leitura WHERE serial=%r'%(cdc))==1):
							c.execute("UPDATE `leitura` SET  `c_ativo` = %r WHERE  `leitura`.`serial` =%r"%(consumo_ativo,cdc))
							c.execute("UPDATE `leitura` SET  `c_reativo` = %r WHERE  `leitura`.`serial` =%r"%(consumo_reativo,cdc))
							c.execute("UPDATE `leitura` SET  `c_capacitivo` = %r WHERE  `leitura`.`serial` =%r"%(consumo_capacitivo,cdc))
							c.execute("UPDATE `leitura` SET  `rssi` = %r WHERE  `leitura`.`serial` =%r"%(rssi,cdc))
							c.execute("UPDATE `leitura` SET  `versao` = %r WHERE  `leitura`.`serial` =%r"%(versao,cdc))
							c.execute("UPDATE `leitura` SET  `serial_blob` = %s WHERE  `leitura`.`serial` =%r"%(cdc,cdc))
							con.commit()
							print ( "TAD  %f Atualizado com sucesso"%(cdc))	
						else:	
							c.execute("INSERT INTO `leitura` VALUES(ID,%r,%r,%r,%r,%r,%r,CURRENT_TIMESTAMP,%s)"%(cdc,versao,rssi,consumo_ativo,consumo_capacitivo,consumo_reativo,cdc))
							con.commit()
							print ( "TAD  %f inserido com sucesso"%(cdc))						
						

						
			else : 
				print ( "Não Achou TA")


"""c.execute("INSERT INTO `leitura` VALUES(30,223,21,23,24,CURRENT_TIMESTAMP)")"""
"""c.execute("INSERT INTO `leitura` VALUES(ID,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)"%(2,3,4,5,6,7))"""
"""c.execute('SELECT * FROM leitura WHERE serial=%s',(3))"""
"""c.execute("UPDATE `leitura` SET  `c_ativo` = %r WHERE  `leitura`.`serial` =%r"%(consumo_reativo,cdc))"""
"""c.execute('SELECT * FROM leitura WHERE serial=%r'%(cdc))"""
	
s


