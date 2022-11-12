# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class DB():
	""" Clase para chequear, crear y borrar usuarios/clave en archivo CSV. """

	def __init__(self, nombre_archivo):
		"""	Constructor de la clase DB.

		Args:
			nombre_archivo: El nombre de archivo en el que se guardará user y pass.
		"""
		
		self.nombre_archivo = nombre_archivo

	def chequear(self, user, clave):
		"""
		Método que lee un archivo CSV y busca un par usuario/clave pasados como argumentos.

		Args:
			user: el usuario a chequear.
			clave: la clave del usuario a chequear.

		Returns:
			- user_encontrado: Un 'True' en caso de coincidencia, 'False' en caso contrario.
			- clave_encontrada: Un 'True' en caso de coincidencia, 'False' en caso contrario.
		"""

		try:
			import csv
			archivo = open(self.nombre_archivo)
			csv_abierto = csv.reader(archivo, delimiter='|')

			user_encontrado = False
			clave_encontrada = False

			if archivo:
				for c, fila in enumerate(csv_abierto):
					if fila[0] == user:
						user_encontrado = True
						if fila[1] == clave:
							clave_encontrada = True
				archivo.close()

			return user_encontrado, clave_encontrada
		
		except IOError as e:
			print("ERROR al leer usuario/clave:", e)
			return False, False


	def crear(self, user, clave):
		"""
		Método que guarda un par usuario/clave en archivo CSV.

		Args:
			user: el nombre de usuario a guardar.
			clave: la clave de usuario a guardar.

		Return:
			True: si la operación fue exitosa.
			False: si hubo un IOError.

		Raises:
			IOError: ERROR al guardar usuario/clave.
		"""
		
		try:
			with open(self.nombre_archivo, 'a') as archivo:
				archivo.writelines([user + '|' + clave + '\n'])
			return True

		except IOError as e:
			print("ERROR al guardar usuario/clave:", e)
			return False


	def borrar(self, user, clave):
		"""
		Método que borra un par usuario/clave en archivo CSV.

		Args:
			user: el nombre de usuario a borrar.
			clave: la clave de usuario a borrar.

		Return:
			True: si la operación fue exitosa.
			False: si hubo un IOError.

		Raises:
			IOError: ERROR al guardar usuario/clave.
		"""
		
		try:
			with open(self.nombre_archivo, 'r+') as archivo:
				todas_lineas = archivo.readlines()
				archivo.seek(0)

				for linea in todas_lineas:
					if not linea.startswith(user):
						archivo.write(linea)

				archivo.truncate()
			return True

		except IOError as e:
			print("ERROR al borrar usuario/clave:", e)
			return False

# FIN