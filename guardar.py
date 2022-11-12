# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class Exportar():
	""" Clase que guarda resultados recibidos en CSV con nombre de fecha y hora actual. """

	def __init__(self, ruta):
		""" Constructor de la clase Exportar. 

		Args:
			ruta: string con ruta para el archivo a guardar.
		"""

		import datetime

		# Variable de estado:
		self.ok = None

		# Guardarmos la ruta completa:
		self.ruta = ruta

		# Generando ruta y nombre de archivo con fecha y hora actual:
		self.nombre_archivo = "resultados_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv" 


	def local(self, resultados, titulo):
		""" Método que guarda una lista de resultados en un archivo CSV local.

		Args:
			resultados: Lista con los resultados a ser guardados en el nuevo CSV.
			titulo: string que se agregará en la 1ra fila del CSV a crear.

		Raise:
			IOError: Si hubo error al crear CSV.
		"""

		try:
			import csv, os

			# Creando y guardando en archivo los resultados:
			with open(self.ruta + self.nombre_archivo, "w", newline="") as archivo:
				archivo.write(titulo + "\n")				# Agregando título.
				csv_abierto = csv.writer(archivo)
				
				pos = 0										# Variable para guardar la posición en archivo.
				for n, linea in enumerate(resultados):
					csv_abierto.writerow(linea)
					pos = archivo.tell() 					# Se guarda la posición en archivo.

				# Borrando la última linea vacía:
				archivo.seek(pos-2) 						# Se parte desde la última posición, se
				archivo.truncate() 							# retrocede 2 caracteres y se trunca archivo.

			self.ok = True
			return self.ok

		except IOError as e:
			print("ERROR al crear CSV:", e)
			return False


	def nombre_completo(self):
		""" Método que simplemente devuelve un nombre de archivo de la clase. 

		Returns:
			archivo: string con el nombre completo de archivo CSV (sin ruta).
			False: en caso de surgir problemas durante la creación del archivo CSV.
		"""
		if self.ok:
			return self.nombre_archivo
		else:
			return False


# FIN