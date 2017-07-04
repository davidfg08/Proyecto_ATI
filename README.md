# Proyecto_ATI

Proyecto de la materia Aplicaciones con Tecnología de Internet en Python Flask y con DB MongoDB

Escenario
El Grupo Docente de ATI (GDATI) ha establecido como mecanismo de evaluación
un proyecto práctico alineado con los objetivos de la materia. Entre los objetivos de
la materia se encuentra que, al finalizar el los estudiantes deben estar en capacidad
de:

● Identificar las etapas del proceso de construcción de aplicaciones con tecnología
Internet, aplicando un método efectivo para el desarrollo de aplicaciones del dominio
de la tecnología Internet.
● Identificar y seleccionar la tecnología adecuada para el desarrollo de aplicaciones
Internet en diferentes escenarios.
● Usar y entender tecnologías del lado cliente y lado servidor para el desarrollo de
aplicaciones Web.

El Grupo Docente de ATI ha propuesto un proyecto que permita diseñar e
implementar una aplicación web con funcionalidades similares a la aplicación web
8tracks.com .

Los requerimientos indispensables a analizar, diseñar, desarrollar e implementar
son los siguientes:

Nota: nos referiremos a “Lista de reproducción” como “Playlist” de ahora en
adelante.

● La aplicación debe proveer una funcionalidad de registro. Para aquellos
usuarios registrados, la aplicación debe proveer la opción de recuperar la
contraseña.

● Cada usuario registrado puede crear una playlist. Las canciones contenidas
en la playlist pueden ser subidas por el propio usuario, o escogidas de una
lista de canciones ya subidas por otros usuarios registrados.

● La aplicación debe proveer una funcionalidad para subir contenido, una vez
que éste sea cargado con éxito, todas las personas podrán ver lo que se ha
subido en ese momento. Los tipos de contenidos a subir son: texto (títulos,
descripciones, URL de Youtube de las canciones) e imagenes (portada de los
playlists).

● Las canciones subidas por los usuarios deben contener una imagen (portada)
y la canción (el URL de Youtube), título de la canción, artista y año de
publicación de la canción, estas canciones deben ser almacenadas en un
pool de la comunidad donde todos los usuarios registrados podrán acceder a
ellas.

● Debe existir una sección donde el usuario registrado pueda crear una nueva
playlist. Al crear una nueva playlist, el usuario debe subir una imagen de
portada (obligatoria), agregar un título (obligatorio), agregar descripción
(opcional), agregar categorías (obligatorio), y agregar canciones a la playlist
que pueden ser escogidas de una lista de canciones de la comunidad, o dar
la capacidad al usuario de subir una canción nueva.

● Al hacer click sobre la playlist, se desplegará una interfaz con una ampliación
de la imagen de portada, el título de la playlist, la lista de canciones que la
compone, nombre del usuario que la creó, la información descriptiva de la
playlist, la/s categoría/s a la que pertenece, una sección de comentarios y un
reproductor donde se reproducirá el playlist, el usuario puede escoger la
canción del playlist que desea escuchar o dejar que el playlist se reproduzca.

● La aplicación poseerá categorías en forma de hashtags para las playlists
como: #r ock, #pop, #punk, #rap, #hiphop,#jazz, #metal, #techno, #house .
Sin embargo, el usuario deberá ser capaz de crear nuevas categorías
personales. Toda playlist debe tener al menos una (1) categoría asociada a
ella.

● La aplicación debe permitir la búsqueda de playlists usando una barra de
búsqueda, mediante las categorías.

● El usuario registrado puede darle “Like” a un playlist para demostrar su
aprobación; de igual forma el usuario puede agregar el playlist a su lista de
favoritos.

● Todo usuario registrado debe tener un perfil en el cual debe mostrar su
información personal, las playlists creadas por el usuario, así como sus
playlists favoritos.

● La aplicación contará con un feed en la página principal el cual mostrará los
playlists con más “likes”, se debe mostrar un cierto número de playlists y
cargar más dinámicamente en caso que el usuario lo desee.

● El usuario no registrado solo puede: ver la página principal, buscar y
escuchar playlists y registrarse.
