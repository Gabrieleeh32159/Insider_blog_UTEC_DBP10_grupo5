# Insider_blog_UTEC_DBP10_grupo5
Proyecto 1 del grupo 5 del laboratorio 1.01 del curso DBP. Insider Blog.

# Nombre del proyecto
El nombre del proyecto es "Insider Blog"

# Integrantes
- Gabriel Espinoza
- Marcelo Zuloeta
- Martín Pérez-Bonany
- Paolo Vásquez

# Descripcion del proyecto
Foro web con la finalidad de conectar universitarios con fines de crear grupos de estudio, resolver problemas específicos y conectar juniors con oportunidades de prácticas laborales.

# Licencia de uso
Este proyecto cuenta con licencia conforme a los términos de la licencia MIT

# Objetivos principales / Mision / Vision
El objetivo principal del proyecto es conectar universitarios de varias casas de estudio en la región.
Nuestra misión es que diversos grupos de universitarios de diferentes universidades puedan conectarse con motivos de estudio o prácticas pre-profesionales.
Nuestra visión es ser el principal portal de conectividad entre universitarios del Perú, ofreciendo un servicio simple pero efectivo y funcional.

# Informacion acerca de las librerias/frameworks/plugins utilizadas en Front-end, Back-end y Base de datos
-vue: framework utilizado para la creación del frontend
-datetime : Para guardar los posts con la fecha de creacion.
-wtforms : Validadores de email, longitud, data requerida, etc para los formularios
-PIL : Para la compresion de imagenes que se usan en los perfiles
-secrets : Para generar una cadena de caracteres aleatorios para serializar
-os : Para usar algunas variables de entorno y unos path para las imagenes

# El nombre del script a ejecutar para iniciar la base de datos con datos
El nombre del script a ejectuar es "app.py"

# Informacion acerca de los API. Requests y Responses de cada endpoint utilizado en el sistema.
endpoints:
- / y /home [None]
- /group/<group_id> [None]
- /about [None]
- /new_post [GET, POST]
- /post/<int:post_id> [GET, POST]
- /post/<int:post_id>/update [GET, POST]
- /post/<int:post_id>/delete [POST]
- /register [GET, POST]
- /login [GET, POST]
- /logout 
- /account [GET, POST]
- /user/<string:username> 
- /create_group/<user_id> [GET, POST]
- /join_group/<user_id> [GET, POST]
- /group/<group_id>/leave [GET, POST]

# Hosts
Localhost
Puerto: 5000

# Forma de autenticacion
- @login.required : flask_login/utils.py para acceder a rutas que necesiten estar loggeado.
Para loggearte, usamos un form donde el usuario ingresa sus datos, vemos si existe el usuario, comprobamos la contrasena encriptada mediante el encriptador y en caso todo este correcto, el log in se hace con
[login_user() : flask_login/utils.py] y despues te envia a la pagina de inicio pero ya loggeado.

# Errores HTTP:
- 500: Utilizado cuando hay algun error en el servidor
- 403: En caso queramos modificar un post que no es nuestro
- 404: En caso entres a un post o usuario que no existe
- 400: El servidor no va a procesar la peticion
- 300: Redireccion
- 200: Conexion satisfactoria
- 100: Continue
