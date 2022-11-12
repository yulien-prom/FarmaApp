# FarmaApp

Archivo: https://github.com/yulien-prom/FarmaApp
Aplicación web realizada como trabajo de final para la materia o unidad curricular de [Programación](https://www.uneti.edu.ve/campus/course/view.php?id=51), la materia es de trayecto 1° de la U.N.E.T.I Universidad Nacional Experimental de las Telecomunicaciones e Informatica *[UNETI](http://www.uneti.edu.ve)*  [Informatica](https://www.uneti.edu.ve/campus/mod/page/view.php?id=986&forceview=1#nav).

* *Alumno: **Victor Manuel D. D.***
* *Profesor: **David S.***
* *Sección: **4A.*** 

![Imagen](https://i.imgur.com/iqwjMnf.jpg)

## Informe

### Funcionamiento:

La aplicación arranca desde el *login*, donde los usuarios registrados pueden ingresan con su nombre de usuario y clave. Se cuenta con la posibilidad de poder registrarse para el caso de los usuarios nuevos en la sección de *registrar* (estas 2 secciones son las únicas visibles en tanto no se ingrese con un usuario y una clave válidas).

* **Nota:** en el archivo [usuario_clave.csv] se pueden ver algunos de los pares usuario/clave registrados originalmente.

Una vez logueado en el sistema, se muestran las últimas ventas registradas desde un archivo CSV principal; desde allí se pueden realizar cualquiera de las 4 consultas solicitadas por el trabajo en la barra de navegación:

* *Productos por Cliente*
* *Clientes por Producto*
* *Productos más vendidos*
* *Clientes que más gastaron*

En cada uno se ofrece la posibilidad de poder descargar en nuestra máquina las consultas efectuadas en formato CSV.

También desde la misma barra de navegación se puede ver en el extremo derecho el nombre del usuario logueado, desde el cual se puede hacer clic para ver las opciones de *cambiar clave* o *salir* del sistema (desloguearse y volver a la sección de login).


### Estructura de la aplicación:

#### [En carpeta raíz]

*  **[app.py]:** el script principal. El mismo inicia importando e instanciando lo siguiente:

  * *Flask*, sus extensiones nativas y las extensiones extra utilizadas (*Flask-Bootstrap, Flask-Script*).
  * Los scripts de python utilizados para realizar las consultas.
  
    También contiene configuraciones varias y las distintas rutas con el origen de los archivos CSV usados y el log de registro de errores.
    
    Su función principal es contener todas las funciones necesarias para redirigir a los templates correspondientes según elija el usuario y las condiciones impuestas de acuerdo al caso (si está logueado, si hay datos disponibles, si la validación fue correcta, etc.)
    

* **[validar.py]:** el script contiene a las clases:

  *  **Csv**: Clase que recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Cuenta con los métodos para abrir el archivo fuente y validar sus campos, fila por fila.

  *  **MiExcepcion**: Clase usada a modo de excepción personalizada en la clase **Csv** cuando surgen en ésta mensajes de error a lo largo de las validaciones, en caso de existir.

* **[consultas.py]:**  el  mismo contiene a las clases:

  *  **Consultas**: Clase que también recibe en su constructor un nombre de archivo como fuente de *datos* y un archivo *log* para guardar errores. Esta misma clase instancia un objeto de la clase **Csv**, y si la validación del CSV en esta última es correcta entonces la clase *Consultas* brinda los métodos necesarios para realizar todas las consultas de datos que se pueden hacer a lo largo del sitio.

  *  **Valores**: Clase que recibe solamente un nombre de campo y que representa en forma de "lista de listas" los resultados utilizados en uno de los métodos de la clase *Consultas*. En concreto, contiene los métodos necesarios para encontrar, sumar, agregar, ordenar/recortar/devolver los resultados en dicha lista.

    
* **[db.py]:** este script contiene a la clase:

  * **DB**: Clase que recibe un nombre de archivo en su constructor y que cuenta con los métodos necesarios para leer y chequear todos los pares usuario/contraseña ya registrados.

* **[formularios.py]**: este contiene a las siguientes clases:
  * **Login**: Clase que contiene los inputs necesarios para el formulario de login al ingresar al sitio.
  
  * **Registro**: Clase que hereda de Login y que contiene los inputs necesarios para el formulario de registro del sitio.
 
  * **Cambio_Clave**: Clase que contiene los inputs necesarios para el formulario de cambio de clave (cuando se está logueado como usuario).

  * **Busqueda**: Clase que contiene los inputs necesarios para el formulario de búsqueda (usado en 2 de las 4 consultas que el sitio brinda).

  *  **Traer**: Clase que contiene los inputs necesarios para el formulario de cantidad a traer (usado en las otras 2 consultas restantes que el sitio brinda).
  
  *  **Local**: Clase que contiene solamente el submit necesario para exportar los resultados a un archivo CSV.

* **[guardar.py]aqui va los enlaces de la cuenta de github**: contiene una única clase:
  * **Exportar**: Clase que guarda resultados recibidos en CSV con nombre de fecha y hora actual.

* **error.log:** El archivo de texto plano que guardará los errores originados durante la validación del CSV, en caso de haberlos. Siempre se sobrescribe en caso de realizarse una nueva consulta, independientemente de si han surgido errores o no.

#### [En carpeta csv]

* **[archivo.csv]:** El fichero de texto plano que contiene toda la información de las ventas realizadas, divididos en campos 5 separados por coma.
La primera fila debe indicar siempre los campos (el orden puede variar y no originará ningún problema) y siempre deberán ser cinco.

  * Código
  * Cliente
  * Producto
  * Cantidad
  * Precio

En caso de que el CSV vengan con campos vacíos o con valores que no correspondan al campo en cuestión, se generará errores que la aplicación notificará en la sección de inicio de usuario.

* **[usuario_clave.csv]:** El ya mencionado archivo en donde se guardan los pares usuario/clave correspondientes.


* **[Carpeta resultados]:** En esta carpeta solo se guardan temporalmente los archivos CSV originados por las consultas descargadas. Su contenido se borrará por completo cuando el usuario se desloguee del sistema.

#### [En carpeta templates]

* **[base.html]:** Contiene el navbar y la división contenedora principal del sitio. Se usa justamente de base para todos los restantes templates. El navbar en si variará su contenido de acuerdo a si existe un user logueado o no. En caso de haberlo, mostrará los links con las distintas consultas disponibles y el nombre del usuario logueado (con la opción de cambiar de clave y la opción de salir).
    

* **[inicio.html]:** Contiene el formulario de logueo para ingresar al sitio.

* **[registro.html]:** Contiene el formulario de registro para registrarse como usuario válido en la aplicación.


* **[usuario.html]:** Recibe al usuario recién logueado con las últimas ventas realizadas (o las que existan) a modo de información útil o relevante.


* **[pxc.html]:** El template con el formulario para obtener los productos por cliente.

* **[cxp.html]:** El template con el formulario para obtener los clientes por producto.

* **[pmv.html]:** El template con el formulario para obtener los productos más vendidos.

* **[cmg.html]:** El template con el formulario para obtener a los clientes que más gastaron.


* **[clave.html]:** Contiene un formulario de cambio de clave para el usuario actualmente logueado.


* **[404.html]:** El template con mensaje de error en caso de no encontrarse la página buscada.

* **[500.html]:** El template con mensaje de error en caso de surgir un error en el servidor.

#### [En carpeta static]

* **[estilos.css]:** El archivo CSS con los estilos propios usados a lo largo del sitio.


* **[jquery.min.js]:** Archivo requerido por Bootstrap.


* Carpeta **[imágenes]:** La carpeta que contiene el icono del sitio más las imágenes usadas para [404.html] y [500.html]


* Carpeta **[bootstrap]:** Carpeta donde se descarga todo el contenido necesario para usar [Bootstrap](http://getbootstrap.com/docs/3.3/getting-started/#download) y [jQuery](http://jquery.com/download/) en nuestra aplicación a modo local (evitando usar el CDN).

## Instalación/Requisitos
En caso de instalar la app desde el código fuente, es necesario tener instalados [Python 3](https://www.python.org/downloads/) y [Flask](http://flask.pocoo.org/)  nuestro sistema operativo.

Además, es necesario también contar con las siguientes extensiones:
  * [Flask_WTF](https://flask-wtf.readthedocs.io/)
  * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/)
  * [Flask-Script](https://flask-script.readthedocs.io/)


(Para más detalles chequear [requirements.txt])

 Se recomienda emplear un entorno virtual como [VirtualEnv](https://virtualenv.pypa.io/) o [VirtualEnvWrapper](https://virtualenvwrapper.readthedocs.io/) para ejecutar la app con dichas extensiones.
