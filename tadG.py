
#!/usr/bin/python
# -*- coding:utf-8 -*-

""" Programa para teste parser

54 41 44 30 00 1C 00 00 00 00 AA 55 00 13 28 72 60 05 0A 02 00 00 01 05 0A 07 FF FF FF 05 0A 0C FF FF FF 33 63 00 
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

medidor = serial.Serial('/dev/ttyUSB0', 9600)

while True:
	time.sleep(1)
	if medidor.inWaiting()> 0:
		if (medidor.read(3)=="TAD"):
			versao = medidor.read(1)
			byte_livre_1 = medidor.read(1)
			rssi = medidor.read(1)
			byte_livre_2 = medidor.read(4)
			preambulo = medidor.read(2)
			cdc = medidor.read(5)
			tam_ativo = medidor.read(1)
			escopo.ativo = medidor.read(2)
			consumo.ativo = medidor.read(ord(tam_ativo) - 2)
			tam_reativo = medidor.read(1)
			escopo_reativo = medidor.read(2)
			consumo_reativo = medidor.read(ord(tam_reativo) - 2)
			tam_capacitivo = medidor.read(1)
			escopo_capacitivo = medidor.read(2)
			consumo_capacitivo = medidor.read(ord(tam_capacitivo) - 2)
			crc = medidor.read(2)
			bcc = medidor.read(1)
			print ( "Achou TAD")
		else : 
			print ( "Não Achou TAD")
	

		

	



