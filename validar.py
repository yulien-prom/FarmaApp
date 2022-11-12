# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

# Clases:
class Csv():
	"""
	La clase que contendrá todos los métodos para validar el CSV (según ejercicio).
	"""
	
	def __init__(self, archivo, log):
		"""	Constructor de la clase Csv.

		Args:
			archivo: El archivo que contiene todo el CSV.
			log: El archivo que guardará todos los mensajes de error, en caso de haberlos.
		"""

		# Variable que constatará si todas la validaciones fueron correctas o no:
		self.ok = None

		# Lista que guardará otras listas con 3 campos: tipo, linea y error:
		self.mensajes_error = []
		
		# Diccionario que guarda la posición relativa de los campos:
		self.campos = {"CODIGO": 0, "CLIENTE": 0, "PRODUCTO": 0, "CANTIDAD": 0, "PRECIO": 0}

		try:
			# Creando un error.log desde cero.
			with open(log, "w") as archivo_log:
				archivo_log.write("")

			# Método que ejecutará todas las validaciones:
			self.validando(archivo)

		except MiExcepcion as e:
			with open(log, "w") as archivo_log:
				for linea in e.mensajes_error:
					archivo_log.write("[Linea " + str(linea[0]) + "] " + linea[1] + "\n")


	def validando(self, nombre_archivo):
		""" Método que realizará las validaciones solicitadas en un CSV, una a la vez.

		Args:
			nombre_archivo: El archivo que contiene todo el CSV.
		 """

		# Abriendo:
		archivo, csv = self.abrir_csv(nombre_archivo)
		
		if archivo:
			# Asumimos que la 1ra fila del CSV contiene los campos correctamente...
			self.obtener_ubicacion_campos(archivo, csv)

			# Realizamos las validaciones:
			self.cant_campos(archivo, csv, len(self.campos))
			self.codigos(archivo, csv, self.campos["CODIGO"])
			self.cantidades(archivo, csv, self.campos["CANTIDAD"])
			self.precios(archivo, csv, self.campos["PRECIO"])

			# Si NO hubo mensajes de error:
			if len(self.mensajes_error) == 0:
				self.ok = True

			# En caso contrario:
			else:
				self.ok = False
				raise MiExcepcion(self.mensajes_error)

		return 0


	def abrir_csv(self, archivo):
		""" Método que abre un archivo CSV para lectura.

		Args:
			nombre_archivo: El archivo que contiene todo el CSV.

		Returns:
			- archivo_abierto: Un objeto open() obtenido a partir de nombre_archivo.
			- None: en caso de surgir FileNotFoundError o PermissionError.
			
			- csv_abierto: Un objeto csv.reader() obtenido a partir del objeto open().
			- None: en caso de surgir IOError. 

		Raises:
			- FileNotFoundError: ERROR: No se encontró el archivo (...).
			- PermissionError: ERROR: No hay permisos para abrir el archivo (...).
		"""

		try:
			import csv
			archivo_abierto = open(archivo, newline="")
			csv_abierto = csv.reader(archivo_abierto, delimiter=",")
			return archivo_abierto, csv_abierto

		except FileNotFoundError:
			self.mensajes.append("ERROR: No se encontró el archivo \"{}\".".format(self.nombre))
			return None, None

		except PermissionError:
			self.mensajes.append("ERROR: No hay permisos para abrir el archivo \"{}\".".format(self.nombre))
			return None, None


	def obtener_ubicacion_campos(self, archivo, csv):
		""" Método que obtiene la 1ra fila de un archivo CSV.
		Se asume que este siempre existe y que sus campos pueden venir en cualquier orden.
		
		Args:
			archivo: El objeto open() abierto.
			csv: El objeto csv.reader() abierto.
		"""

		for c, fila in enumerate(csv):
			if c == 0:  								# Si es la 1ra fila...
				for posicion, campo in enumerate(fila):
					campo = campo.upper().strip()
					self.campos[campo] = posicion
		
		archivo.seek(0)
		return 0


	def cant_campos(self, archivo, csv, cant_campos):
		""" Método que chequea la cantidad de campos de todas las filas de un archivo CSV.
		
		Args:
			archivo: El objeto open() abierto.
			csv: El objeto csv.reader() abierto.
			cant_campos: Un int que contiene la cantidad de campos.
		"""
	
		for c, fila in enumerate(csv):
			if c > 0:									# Si es filas de datos...
				if len(fila) != cant_campos:
					self.mensajes_error.append([c+1, "Se encontró distinta cantidad de campos.", "Campos"])
					estado = False

		archivo.seek(0)
		return 0


	def codigos(self, archivo, csv, codigo):
		""" Método que chequea los campos CODIGO de un CSV en caso de estar vacíos.

		Args:
			archivo: El objeto open() abierto.
			csv: El objeto csv.reader() abierto.
			codigo: Un int con el valor de 'CODIGO' en el diccionario 'campos'.
		"""

		for c, fila in enumerate(csv):
			if c > 0:									# Si es filas de datos...
				if fila[codigo] == "" or fila[codigo] == " ":
					self.mensajes_error.append([c+1, "Se encontró un código vacío.","Códigos"])

		archivo.seek(0)
		return 0


	def cantidades(self, archivo, csv, cantidad):
		""" Método que chequea los campos CANTIDAD de un CSV en caso de no contener cantidades enteras.

		Args:
			archivo: El objeto open() abierto.
			csv: El objeto csv.reader() abierto.
			cantidad: Un int con el el valor de 'CANTIDAD' en el diccionario 'campos'.
		"""

		for c, fila in enumerate(csv):
			if c > 0:									# Si es filas de datos...
				parte_entera = 0
				parte_fraccion = 0
				error = False

				try:
					# Traemos string, la pos. del pto. decimal y de ahí la parte entera y frac.:
					valor = fila[cantidad]
					p = valor.index(".")
					parte_entera = int(valor[:p])
					parte_fraccion = int(valor[p + 1:])

				except (ValueError, IndexError):
					self.mensajes_error.append([c+1, "El campo cantidad no contiene un valor entero.", "Cantidades"])

		archivo.seek(0)
		return 0


	def precios(self, archivo, csv, precio):
		""" Método que chequea los campos PRECIO de un CSV en caso de no contener valores decimales.

		Args:
			archivo: El objeto open() abierto.
			csv: El objeto csv.reader() abierto.
			precio: Un int con el el valor de 'PRECIO' en el diccionario 'campos'.
		"""

		for c, fila in enumerate(csv):
			if c > 0:									# Si es filas de datos...
				parte_entera = 0
				parte_fraccion = 0

				# Obtenemos string y de ahí sacamos parte entera y fraccionaria:
				try:
					valor = fila[precio]
					parte_entera = int(valor[:-3])
					parte_fraccion = int(valor[-2:])

				except (ValueError, IndexError):
					self.mensajes_error.append([c+1, "El campo precio no contiene un un valor decimal.","Precios"])

		archivo.seek(0)
		return 0


class MiExcepcion(Exception):
	""" Clase de excepción personalizada usada en la clase Csv."""

	def __init__(self, mensajes_error):
		""" Constructor de la clase MiExcepción
		
		Args:
			mensajes_error: La lista que contiene todos los mensajes de error generados a lo
			largo de todas las verificaciones realizadas.
		"""

		self.mensajes_error = mensajes_error


# FIN