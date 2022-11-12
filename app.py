# -----------------------------------------------------------------------------
# Final de Paradigmas de Programación y Estructura de Datos
# (1° Año, 2° Cuatr. - 2017)
#
# -	Alumno: Federico H. Cacace
# -	Profesor: Leandro E. Colombo Viña
# -----------------------------------------------------------------------------

from flask import Flask, render_template, redirect, url_for, flash, session, send_file
from flask_bootstrap import Bootstrap, StaticCDN
from flask_script import Manager
import formularios, consultas, db, guardar


# Creando objetos flask:
app = Flask(__name__)
manager = Manager(app)
bs = Bootstrap(app)


# Constantes con rutas y nombres de archivos:
RUTA = ""
ERROR = RUTA + "error.log"
ARC_CSV = RUTA + "csv/archivo.csv"
USER_CLAVE = RUTA + "csv/usuario_clave.csv"
TEMP = "csv/resultados/"


# App.config:
app.config["SECRET_KEY"] = "UnaClaveSecreta"					# Clave random para formularios de Flask-WTF.
app.config["BOOTSTRAP_SERVE_LOCAL"] = True 						# Para activar versión local de Bootstrap.
app.config["BOOTSTRAP_QUERYSTRING_REVVING"] = False		# Para quitar el "?bootstrap=..." cuando se
																											# buscan los archivos de bootstrap locales.

# App.extensions:
app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()	# Para poder usar archivo jQuery local.


# Funciones:
@app.route("/login", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def inicio():
	""" Función que lleva a inicio.html o usuario.html según condiciones. """
	
	# Si existe algún 'user' en sesión:
	if session.get("user"):
		return redirect(url_for("usuario"))

	# En caso de no haber usuario logueado, se prosigue:
	else:
		log = formularios.Login()
		
		# Si se presionó el botón enviar:
		if log.validate_on_submit():

			bd = db.DB(USER_CLAVE)
			user, clave = bd.chequear(log.usuario.data, log.clave.data)

			if user:
				if clave:
					session["user"] = log.usuario.data
					return redirect(url_for("usuario"))

				# Si la clave no corresponde con ese usuario:
				else:
					error = "clave inválida"
					return render_template("inicio.html",
											error=error,
											login=log)

			# Si el usuario no existe en la DB:
			else:
				error = "<b>{}</b> no es un usuario registrado".format(log.usuario.data)
				return render_template("inicio.html",
										error=error,
										login=log)

		# En caso de ingresar por primera vez:
		return render_template("inicio.html",
								login=log)


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
	""" Función que lleva a registro.html, inicio.html o usuario.html según condiciones. """

	# Si existe algún 'user' en sesión:
	if session.get("user"):
		return redirect(url_for("usuario"))

	# En caso de no haber usuario logueado, se prosigue:
	else:
		registro = formularios.Registro()
		
		# Si se presionó el botón enviar:
		if registro.validate_on_submit():
			
			# Si los campos de claves son distintos entre si:
			if registro.clave.data != registro.repetir_clave.data:
				error = "Las claves ingresadas son distintas entre si."
				return render_template("registro.html",
										error=error,
										registro=registro)
			
			# Si ambas claves son iguales, se prosigue:
			else:
				bd = db.DB(USER_CLAVE)
				user, clave = bd.chequear(registro.usuario.data, registro.clave.data)
				
				# Si ya existe usuario:
				if user:
					error = "<b>{}</b> ya es un usuario registrado".format(registro.usuario.data)
					return render_template("registro.html",
											error=error,
											registro=registro)

				# En caso contrario, se registra y se redirecciona a inicio:
				registro_ok = bd.crear(registro.usuario.data, registro.clave.data)
				if registro_ok:
					flash("El usuario ha sido registrado con éxito")
					return redirect(url_for("inicio"))

				# Si surgió algún error durante el registro, se notifica:
				else:
					error = "Hubo un error al intentar registrarse en la DB."
					return render_template("registro.html",
											error=error,
											registro=registro)

		# En caso de ingresar por primera vez:
		return render_template("registro.html",
								registro=registro)


@app.route("/usuario", methods=["GET", "POST"])
def usuario():
	""" Función que lleva a usuario.html o inicio.html según condición. """

	# SI hay 'user' en sesión:
	if session.get("user"):
		# Creando objeto consulta:
		consulta = consultas.Consultas(ARC_CSV, ERROR)

		# Chequeando que validación del CSV haya sido correcta:
		if consulta.csv.ok:

			# Borrando variable de error, si aún estaba fijada:
			session.pop("error_csv", None)

			CANTIDAD=5
			resultados, nro_filas = consulta.ultimos_resultados(CANTIDAD)
	
			return render_template("usuario.html",
									usuario=True,
									resultados=resultados,
									nro_filas=nro_filas,
									cantidad=CANTIDAD)

		# En caso de que el CSV no se haya validado correctamente:
		else:
			session["error_csv"] = True
			error = "Surgieron errores durante la validación del CSV"
			return render_template("usuario.html",
									usuario=True,
									error=error,
									mensajes_error=consulta.csv.mensajes_error)
	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/clientes", methods=["GET", "POST"])
def pxc():
	""" Función que lleva a pxc.html o inicio.html según determinadas condiciones. """
	
	# SI hay 'user' en sesión:
	if session.get("user"):

		# Creando todos objetos formularios necesarios:
		busqueda = formularios.Busqueda()
		bajar = formularios.Local()

		# Creando objeto consulta y obteniendo sugerencias:
		consulta = consultas.Consultas(ARC_CSV, ERROR)
		sugerencias = consulta.listar_x("CLIENTE")

		# Si se presionó el botón de buscar resultados:
		if busqueda.validate_on_submit() and busqueda.submit.data:

			# Obteniendo palabra desde input del formulario (si hay):
			if busqueda.buscar.data:
				pxc.palabra = busqueda.buscar.data.lower()

			# Obteniendo resultados:
			pxc.resultados, pxc.columnas = consulta.listar_x_en_y(pxc.palabra, "PRODUCTO", "CLIENTE")
			
			# Si hubo resultados:
			if len(pxc.resultados) > 1:
				return render_template("pxc.html",
										busqueda_pxc=busqueda,
										bajar=bajar,
										sugerencias=sugerencias,
										resultados=pxc.resultados,
										columnas=pxc.columnas)
			# Si NO hubo resultados: 
			else:
				error = "No hubo resultados con ese término"
				return render_template("pxc.html",
										error=error,
										busqueda_pxc=busqueda,
										sugerencias=sugerencias)					

		# Si se presionó el botón de descargar resultados:
		elif bajar.validate_on_submit() and bajar.submit.data:

			# Si no hubo problemas se descargan los resultados en un CSV:
			import datetime as dt
			fecha = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
			titulo = "[Consulta: Productos por Cliente] [Usuario: {}] [Fecha: {}]".format(session["user"], fecha)
			
			exportar = guardar.Exportar(RUTA + TEMP)
			exp_ok = exportar.local(pxc.resultados, titulo)

			# Si se pudo crear CSV:
			if exp_ok:
				session["nombre"] = exportar.nombre_completo()
				session["ruta"] = exportar.ruta
				return redirect(url_for("descargar"))
			
			# Caso contrario, se muestra mensaje de error:
			else:
				error = "Hubo un problema al intentar crear el archivo CSV."
				return render_template("pxc.html",
										error=error,
										busqueda_pxc=busqueda,
										sugerencias=sugerencias)
	
		# Si no se envia aún ninguna búsqueda:
		else:	
			return render_template("pxc.html",
									busqueda_pxc=busqueda,
									sugerencias=sugerencias)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/productos", methods=["GET", "POST"])
def cxp():
	""" Función que lleva a cxp.html o inicio.html según determinadas condiciones. """
	
	# SI hay 'user' en sesión:
	if session.get("user"):

		# Creando todos objetos formularios necesarios:
		busqueda = formularios.Busqueda()
		bajar = formularios.Local()

		# Creando objeto consulta y obteniendo sugerencias:
		consulta = consultas.Consultas(ARC_CSV, ERROR)
		sugerencias = consulta.listar_x("PRODUCTO")

		# Si se presionó el botón de buscar resultados:
		if busqueda.validate_on_submit() and busqueda.submit.data:

			# Obteniendo palabra desde input del formulario (si hay):
			if busqueda.buscar.data:
				cxp.palabra = busqueda.buscar.data.lower()

			# Obteniendo resultados:
			cxp.resultados, cxp.columnas = consulta.listar_x_en_y(cxp.palabra, "CLIENTE", "PRODUCTO")
			
			# Si hubo resultados:
			if len(cxp.resultados) > 1:
				return render_template("cxp.html",
										busqueda_cxp=busqueda,
										bajar=bajar,
										sugerencias=sugerencias,
										resultados=cxp.resultados,
										columnas=cxp.columnas)
			# Si NO hubo resultados: 
			else:
				error = "No hubo resultados con ese término"
				return render_template("cxp.html",
										error=error,
										busqueda_cxp=busqueda,
										sugerencias=sugerencias)					

		# Si se presionó el botón de descargar resultados:
		elif bajar.validate_on_submit() and bajar.submit.data:

			# Si no hubo problemas se descargan los resultados en un CSV:
			import datetime as dt
			fecha = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
			titulo = "[Consulta: Clientes por Producto] [Usuario: {}] [Fecha: {}]".format(session["user"], fecha)
			
			exportar = guardar.Exportar(RUTA + TEMP)
			exp_ok = exportar.local(cxp.resultados, titulo)

			# Si se pudo crear CSV:
			if exp_ok:
				session["nombre"] = exportar.nombre_completo()
				session["ruta"] = exportar.ruta
				return redirect(url_for("descargar"))
			
			# Caso contrario, se muestra mensaje de error:
			else:
				error = "Hubo un problema al intentar crear el archivo CSV."
				return render_template("cxp.html",
										error=error,
										busqueda_cxp=busqueda,
										sugerencias=sugerencias)
	
		# Si no se envia aún ninguna búsqueda:
		else:	
			return render_template("cxp.html",
									busqueda_cxp=busqueda,
									sugerencias=sugerencias)

	# Si NO hay 'user' en sesión:
	else:
		return redirect(url_for("inicio"))


@app.route("/masvendidos", methods=["GET", "POST"])
def pmv():
	""" Función que lleva a pmv.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):

		# Creando todos objetos formularios necesarios:
		traer = formularios.Traer()
		bajar = formularios.Local()

		# Si se presionó el botón de buscar resultados:
		if traer.validate_on_submit() and traer.submit.data:

			# Obteniendo palabra desde un IntegerField del formulario (si hay datos):
			if traer.buscar.data:
				pmv.cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			pmv.resultados, pmv.columnas = consulta.listar_los_mas_x(pmv.cantidad, "PRODUCTO", "CANTIDAD")

			return render_template("pmv.html",
									traer_pmv=traer,
									bajar=bajar,
									resultados=pmv.resultados,
									columnas=pmv.columnas)

		# Si se presionó el botón de guardar resultados:
		elif bajar.validate_on_submit() and bajar.submit.data:

			# Si no hubo problemas se descargan los resultados en un CSV:
			import datetime as dt
			fecha = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
			titulo = "[Consulta: Productos más vendidos] [Usuario: {}] [Fecha: {}]".format(session["user"], fecha)
			
			exportar = guardar.Exportar(RUTA + TEMP)
			exp_ok = exportar.local(pmv.resultados, titulo)

			# Si se pudo crear CSV:
			if exp_ok:
				session["nombre"] = exportar.nombre_completo()
				session["ruta"] = exportar.ruta
				return redirect(url_for("descargar"))
			
			# Caso contrario, se muestra mensaje de error:
			else:
				error = "Hubo un problema al intentar crear el archivo CSV."
				return render_template("pmv.html",
										error=error,
										traer_pmv=traer)

		# Si NO se envia aún ninguna búsqueda:
		else:
			return render_template("pmv.html",
									traer_pmv=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/masgastaron", methods=["GET", "POST"])
def cmg():
	""" Función que lleva a cmg.html o inicio.html según si hay sesión abierta o no. """

	# SI hay 'user' en sesión:
	if session.get("user"):

		# Creando todos objetos formularios necesarios:
		traer = formularios.Traer()
		bajar = formularios.Local()

		# Si se presionó el botón de buscar resultados:
		if traer.validate_on_submit() and traer.submit.data:

			# Obteniendo palabra desde un IntegerField del formulario (si hay datos):
			if traer.buscar.data:
				cmg.cantidad = traer.buscar.data

			# Creando objeto consulta y obteniendo resultados:
			consulta = consultas.Consultas(ARC_CSV, ERROR)
			cmg.resultados, cmg.columnas = consulta.listar_los_mas_x(cmg.cantidad, "CLIENTE", "PRECIO")

			return render_template("cmg.html",
									traer_cmg=traer,
									bajar=bajar,
									resultados=cmg.resultados,
									columnas=cmg.columnas)

		# Si se presionó el botón de guardar resultados:
		elif bajar.validate_on_submit() and bajar.submit.data:

			# Si no hubo problemas se descargan los resultados en un CSV:
			import datetime as dt
			fecha = dt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
			titulo = "[Consulta: Clientes que más gastaron] [Usuario: {}] [Fecha: {}]".format(session["user"], fecha)
			
			exportar = guardar.Exportar(RUTA + TEMP)
			exp_ok = exportar.local(cmg.resultados, titulo)

			# Si se pudo crear CSV:
			if exp_ok:
				session["nombre"] = exportar.nombre_completo()
				session["ruta"] = exportar.ruta
				return redirect(url_for("descargar"))
			
			# Caso contrario, se muestra mensaje de error:
			else:
				error = "Hubo un problema al intentar crear el archivo CSV."
				return render_template("cmg.html",
										error=error,
										traer_cmg=traer)

		# Si NO se envia aún ninguna búsqueda:
		else:
			return render_template("cmg.html",
									traer_cmg=traer)

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route('/descargar')
def descargar():
	""" Función que permite descargar un CSV determinado. """

	# SI hay 'user' en sesión:
	if session.get("user"):

		# SI están todas las sesiones ruta y nombre:
		if session.get("ruta") and session.get("nombre"):
			
			# Guardando ruta:
			nombre = session["nombre"]
			archivo = session["ruta"] + session["nombre"]

			# Borrando las sesiones ruta y nombre:
			session.pop("ruta", None)
			session.pop("nombre", None)

			# Descargando archivo:
			return send_file(archivo,
						 	 as_attachment=True,
							 attachment_filename=nombre,
							 cache_timeout=5)

		# En caso contrario, volver a usuario.html:
		else:
			return redirect(url_for("usuario"))

	# Si NO hay 'user' en sesión:
	else:										
		return redirect(url_for("inicio"))


@app.route("/clave", methods=["GET", "POST"])
def clave():
	""" Función que lleva a clave.html o inicio.html según condiciones. """

	# Si no existe algún 'user' en sesión, se redirige a inicio:
	if not session.get("user"):
		return redirect(url_for("inicio"))

	# En caso de haberlo, se prosigue:
	else:
		cambio = formularios.Cambio_Clave()

		# Si se presionó el botón enviar:
		if cambio.validate_on_submit():

			bd = db.DB(USER_CLAVE)
			user, clave = bd.chequear(session.get("user"), cambio.vieja_clave.data)

			# Si la vieja clave es la correcta, se prosigue:
			if clave:
				# Si las nuevas claves son ambas idénticas, entonces se procede a cambiar:
				if cambio.nueva_clave.data == cambio.confirmar_nueva_clave.data:

					borrar_ok = bd.borrar(session.get("user"), cambio.vieja_clave.data)
					agregar_ok = bd.crear(session.get("user"), cambio.nueva_clave.data)

					# Si la operación de cambiar ha sido exitosa:
					if borrar_ok and agregar_ok:
						mensaje = "La clave ha sido cambiada con éxito"
						return render_template("clave.html",
												mensaje=mensaje,
												cambio=cambio)
					else:
						error = "Hubo un error al intentar cambiar claves en DB."
						return render_template("clave.html",
												error=error,
												cambio=cambio)
				else:
					error = "La nuevas claves ingresadas son distintas entre si"
					return render_template("clave.html",
											error=error,
											cambio=cambio)

			# Si la clave no corresponde con ese usuario:
			else:
				error = "La clave actual es inválida"
				return render_template("clave.html",
										error=error,
										cambio=cambio)


		# En caso de ingresar por primera vez:
		return render_template("clave.html",
								cambio=cambio)


@app.route("/salir")
def salir():
	""" Función que desloguea al usuario actual y lleva a inicio.html """

	# SI hay 'user' en sesión:
	if session.get("user"):

		# Borrando todos los archivos CSV en carpeta resultados:
		import sys, os

		directorio = RUTA + TEMP
		todos_archivos = os.listdir(directorio)

		for archivo in todos_archivos:
			if archivo.endswith(".csv"):
				os.remove(os.path.join(directorio, archivo))

		# Quitando finalmente sesión user:
		session.pop("user", None)
		flash("Usuario deslogueado")

	# Haya o no sesión abierta, se retorna a inicio.html:
	return redirect(url_for("inicio"))


@app.errorhandler(404)
def no_encontrado(e):
	""" Función que lleva a 404.html en caso de no encontrar la página solicitada. """
	return render_template("404.html"), 404


@app.errorhandler(500)
def error_servidor(e):
	""" Función que lleva a 500.html en caso de surgir algún error en el servidor. """
	return render_template("500.html"), 500


# Iniciando:
if __name__ == "__main__":
	manager.run()


# FIN