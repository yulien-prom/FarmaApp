# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

class Consultas():
	""" Clase que contiene los métodos para realizar las consultas solicitadas. """

	def __init__(self, archivo, log):
		""" Constructor de la clase Consultas. 

		Args:
			archivo: El archivo que contiene todo el CSV.
			log: El archivo que guardará todos los mensajes de error, en caso de haberlos.
		"""

		import validar

		self.archivo = archivo
		self.log = log

		# Creando objeto 'Csv' para ser usado en 'Consultas':
		self.csv = validar.Csv(self.archivo, self.log)

		# 'self.csv.ok' contendrá el estado de la validación del CSV.

	
	def listar_x(self, campo):
		""" Método que busca y devuelve filas del campo buscado en un CSV.

		Args:
			campo: Un nombre del campo sobre el que se buscará sus contenidos.

		Returns:
			resultados: Todas las filas pero solo con el contenido del campo pasado.
		"""

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo = self.csv.campos[campo]

		archivo, csv = self.csv.abrir_csv(self.archivo)
		
		resultados = []
		
		for c, fila in enumerate(csv):
			if c > 0 and fila[nro_campo] not in resultados:
				resultados.append(fila[nro_campo])

		archivo.seek(0)
		return resultados


	def listar_x_en_y(self, palabra, campo1, campo2):
		""" Método que busca y devuelve filas de un CSV a partir de una palabra que	concuerde
		con el contenido de un campo.

		Args:
			palabra: Una palabra recibida desde formulario html a buscar en campo2.
			campo1: Un nombre del campo que debe coincidir con alguno del diccionario 'campos'.
			campo2: Otro nombre del campo que debe coincidir con alguno del diccionario 'campos'.

		Returns:
			resultados: Las filas en donde hubo coincidencias de 'palabra' con 'campo2'.
			columnas: Una lista con las posiciones de columna de las proceden campo1 y campo2.
		"""

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo1 = self.csv.campos[campo1]
		nro_campo2 = self.csv.campos[campo2]
		columnas = [nro_campo1, nro_campo2]

		archivo, csv = self.csv.abrir_csv(self.archivo)
		
		resultados = []
		
		for c, fila in enumerate(csv):
			if c == 0:
				resultados.append(fila)
			else:
				if palabra.lower() in fila[nro_campo2].lower():
					resultados.append(fila)

		archivo.seek(0)
		return resultados, columnas


	def listar_los_mas_x(self, cantidad, campo1, campo2):
		""" Método que busca y muestra en pantalla los N elementos del 'campo1' que más suman
		del	"campo2". 

		Args:
			campo1: Un nombre del campo (que debe coincidir con alguno del diccionario 'campos').
			campo2: Otro nombre del campo (que debe coincidir también con el diccionario 'campos').
			cantidad: Un int para delimitar la cantidad de resultados obtenidos.

		Returns:
			resultados: Las filas en donde hubo coincidencias de 'palabra' con 'campo2'.
			columnas: Una lista con las posiciones de columna de las proceden campo1 y campo2.
		"""

		# Obtenemos las ubicaciones de los campos ya sacados en 'validar.py':
		nro_campo1 = self.csv.campos[campo1]
		nro_campo2 = self.csv.campos[campo2]
		columnas = [nro_campo1, nro_campo2]

		archivo, csv = self.csv.abrir_csv(self.archivo)

		valores = Valores(campo2)

		# Recorremos CSV y agregamos todas las filas al objeto 'valores':
		for c, fila in enumerate(csv):
			if c > 0:
				valores.agregar(fila[nro_campo1], fila[nro_campo2])

		# Obteniendo la lista final de resultados:
		resultados = valores.ordenar_recortar_y_devolver(cantidad)

		archivo.seek(0)
		return resultados, columnas


	def ultimos_resultados(self, cantidad=5):
		""" Método que devuelve los últimos 5 resultados de un CSV .
		
		Args:
			cantidad: Un nombre del campo que debe coincidir con alguno del diccionario
				'campos' de la clase. Valor por defecto: 5.

		Returns:
			resultados: Una lista con la 1ra fila + los últimos resultados del CSV.
			nro_fila: Un Int con el número de fila del CSV desde donde se empiezan a obtener
				los resultados.
			cantidad: El int que se pasó como argumento y que determina la cantidad de
				resultados a traer.
		"""

		archivo, csv = self.csv.abrir_csv(self.archivo)

		resultados = []

		# Obtenemos el contador de filas de resultados (descontando la 1ra fila):
		total_filas = len(list(csv)[1:])
		archivo.seek(0)


		# Recorremos CSV para agregar de las últimas filas del CSV solo la cantidad de filas pasada:
		contador = 0
		for fila in reversed(list(csv)[1:]):
			if contador < cantidad:
				resultados.append(fila)
				contador = contador + 1
		archivo.seek(0)

		# Recorremos de nuevo para agregar la 1ra fila:
		for c, fila in enumerate(csv):			
			if c == 0:
				resultados.append(fila)
				break
		archivo.seek(0)

		# Obteniendo nro_fila según condiciones:
		nro_fila = 0
		if cantidad <= total_filas:
			nro_fila = total_filas - cantidad
		else:
			nro_fila = 0

		resultados = reversed(resultados)
		return resultados, nro_fila
			

class Valores():
	""" Clase que representa valores usados en método de la clase Consultas """

	def __init__(self, campo):
		""" Constructor de la clase Valores.
		Args:
			campo: String que indica si los valores a trabajar son del tipo 'cantidad' o 'precio'.
		"""
		self.campo = campo
		self.resultados = []


	def encontrar(self, elemento):
		""" Método que busca un elemento a una lista
		
		Args:
			elemento: String que describe el elemento a buscar.

		Returns:
			respuesta: booleando que describe el éxito de la búsqueda.
		"""
		respuesta = False
		for par in self.resultados:
			if elemento in par:
				resultado = True
		return respuesta


	def sumar(self, elemento, valor):
		""" Método que suma un valor dentro de un par elemento-valor preexistente en una lista.
		
		Args:
			elemento: string que describe el valor guardado.
			valor: float que representa el valor a sumar al par elemento-valor existente.
		"""

		for par in self.resultados:
			if elemento in par:
				par[1] = par[1] + valor

		return 0


	def agregar(self, elemento, valor):
		""" Método que agrega un par elemento-valor a una lista.
		
		Args:
			elemento: string que describe el valor a guardar.
			valor: float que representa el valor del elemento.
		"""

		# Se intenta castear elemento según campo recibido:
		try:
			if self.campo == 'PRECIO':
				valor = float(valor)
			else:
				valor = int(float(valor))

		except ValueError:
			valor = "ERROR"

		# Si se encuentra el elemento en la lista se lo suma:
		if self.encontrar(elemento):
			self.sumar(elemento, valor)
		
		# En caso de no estarlo, se lo agrega:
		else:
			self.resultados.append([elemento, valor])
		
		return 0


	def ordenar_recortar_y_devolver(self, cantidad):
		""" Método que ordena por valor la lista interna de la clase y se devuelve todo su contenido.
		
		Args: 
			cantidad: La cantidad de elementos que se devolverá de la lista de la clase.

		Returns:
			self.resultados: la lista de la clase que representa pares elemento-valor.
		"""

		self.resultados.sort(key=lambda valor:valor[1], reverse=True)
		if cantidad <= len(self.resultados):
			self.resultados = self.resultados[0:cantidad]

		return self.resultados


# FIN