from flask import Flask, render_template, request, redirect, url_for, json
from pymongo import *
from bson import json_util, ObjectId
from werkzeug import secure_filename
import os, sys

UPLOAD_FOLDER = 'static/imagenes'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, template_folder = 'templates', static_folder = 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MongoDB Connection with PyMongo
client = MongoClient()
db = client.Proyecto
global Usuario_Activo

def try_int(x):
    try:
        return int(x)
    except ValueError:
        return x

# Routes Definition
@app.route('/')
def index(err=None):
	Playlist = db.playlist.find().sort([("me_gusta",-1)])
	Playlist_aux = db.playlist.find().sort([("me_gusta",-1)])
	Playlist_Totales = db.playlist.find().count()
	Mis_json = json.dumps(list(Playlist_aux))

	return render_template('home.html', json1 = Playlist, json2 = Mis_json, cantidad = 6, Total = Playlist_Totales)

@app.route('/registro', methods=['POST'])
def registro():
	usuario = request.form['Nombre']
	email  = request.form['Correo']
	password1  = request.form['Contrasena1']
	password2  = request.form['Contrasena2']
	Palabra = request.form['PalabraS']
	total = db.usuarios.find({}).count() + 1
	
	os.makedirs('static/imagenes/Usuarios/' + str(total) + '/Playlist')
	os.makedirs('static/imagenes/Usuarios/' + str(total) + '/Canciones')

	db.usuarios.insert({"_id":total, 'name':usuario, 'imagen':"perfil1.jpg", 'correo':email , 'contrasena':password1, 'palabra_secreta':Palabra})
	
	return redirect(url_for('index'))

@app.route('/buscar', methods=['POST'])
def buscar(err=None):
	Busqueda = request.form['Busqueda']
	Tipo_B = request.form['Tipo']
	Auxiliar_1 = Busqueda.split(' ')
	Playlist = db.playlist.find({"categorias":{"$in":Auxiliar_1}})
	Playlist_aux = db.playlist.find({"categorias":{"$in":Auxiliar_1}})
	Playlist_Totales = db.playlist.find({"categorias":{"$in":Auxiliar_1}}).count()
	Mis_json = json.dumps(list(Playlist_aux))
	global Usuario_Activo

	if int(Playlist_Totales) > 0:
		if int(Tipo_B) == 1:		
			x = int(Usuario_Activo)
			datos = db.usuarios.find_one({"_id": x})
			return render_template('buscar_sesion.html', info = datos, json1 = Playlist, json2 = Mis_json, cantidad = 6, Total = Playlist_Totales)

		return render_template('buscar_noSesion.html', json1 = Playlist, json2 = Mis_json, cantidad = 6, Total = Playlist_Totales)

	if int(Tipo_B) == 1:
		x = int(Usuario_Activo)
		datos = db.usuarios.find_one({"_id": x})
		return render_template('buscar_noR.html', info = datos)

	return render_template('buscar_noR_s.html')

@app.route('/principal')
def principal(err=None):
	Playlist = db.playlist.find().sort([("me_gusta",-1)])
	Playlist_aux = db.playlist.find().sort([("me_gusta",-1)])
	Playlist_Totales = db.playlist.find().count()
	Mis_json = json.dumps(list(Playlist_aux))

	global Usuario_Activo
	x = int(Usuario_Activo)

	datos = db.usuarios.find_one({"_id": x})

	return render_template('principal_usuario.html', info = datos, json1 = Playlist, json2 = Mis_json, cantidad = 6, Total = Playlist_Totales)

@app.route('/recuperar', methods=['POST'])
def recuperar(err=None):
	Palabra = request.form['palabra']
	usuario = request.form['Usuario']
	temporal = db.usuarios.find_one({ "correo": usuario })
	
	
	if temporal["palabra_secreta"] == Palabra:
		global Usuario_Activo
		Usuario_Activo = temporal["_id"]
		return redirect(url_for('principal'))
	return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login(err=None):
	usuario = request.form['Usuario']
	password  = request.form['pass']
	temporal = db.usuarios.find_one({ "correo": usuario })
	
	
	if temporal["contrasena"] == password:
		global Usuario_Activo
		Usuario_Activo = temporal["_id"]
		return redirect(url_for('principal'))
	return redirect(url_for('index'))


@app.route('/Cancion')
def Cancion(err=None):
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})
	
	return render_template('subir_contenido.html', info = datos)


@app.route('/Crear_Cancion', methods=['POST'])
def Crear_Cancion(err=None):
	global Usuario_Activo
	file = request.files['imagen']
	Titulo = request.form['titulo']
	URL  = request.form['url']
	Artista  = request.form['artista']
	Anno  = request.form['año']
	total = db.canciones.find({}).count() + 1

	temp1, idfinal = URL.split("=")

	filename = secure_filename(file.filename)
	UPLOAD_FOLDER = 'static/imagenes/Usuarios/'+ str(Usuario_Activo) + '/' + 'Canciones'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	db.canciones.insert({"_id":total , 'titulo':Titulo , 'url':idfinal , 'imagen':filename , 'artista':Artista, 'anno':Anno , 'playlists':[] })
	
	return redirect(url_for('principal'))

@app.route('/Playlist')
def Playlist():
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})
	
	aux = db.canciones.find({})
	aux2 = db.canciones.find({})
	total = db.canciones.find({}).count()
	cant = json.dumps(list(aux2))
	return render_template('crear_playlist.html', info = datos, json1 = aux, json2 = cant, cantidad = 5, Total = total)

@app.route('/Crear_Playlist', methods=['POST'])
def Crear_Playlist(err=None):
	global Usuario_Activo
	file = request.files['imagen']
	Titulo = request.form['titulo']
	Descripcion = request.form['descripcion']
	Categorias = request.form['categorias']
	Canciones = request.form['canciones']
	Temporal = Categorias.replace(' ','')
	Auxiliar_1 = Temporal.split(',')
	Auxiliar_2 = Canciones.split(',')
	total = db.playlist.find({}).count() + 1	
	
	filename = secure_filename(file.filename)
	UPLOAD_FOLDER = 'static/imagenes/Usuarios/'+ str(Usuario_Activo) + '/Playlist'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	for x in Auxiliar_2:
		temporal = db.canciones.find_one({"_id":int(x)})
		Playlist_viejas = temporal["playlists"]
		Playlist_viejas.append(total)
		db.canciones.update({"_id":int(x)},{"$set":{'playlists':Playlist_viejas}})

	db.playlist.insert({"_id":total, 'titulo':Titulo, 'descripcion':Descripcion, 'imagen':filename, 'categorias':Auxiliar_1, 'canciones':Auxiliar_2, 'usuario':Usuario_Activo, 'me_gusta':0, 'favorito':[], 'usuario_like':[]})
	return redirect(url_for('principal'))


@app.route('/mis_playlist')
def mis_playlist(err=None):
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})

	aux = db.playlist.find({'usuario':Usuario_Activo})
	aux2 = db.playlist.find({'usuario':Usuario_Activo})
	Mis_play = db.playlist.find({'usuario':Usuario_Activo}).count()
	Mis_json = json.dumps(list(aux2))
	return render_template('modificar_playlist.html', info = datos, json1 = aux, json2 = Mis_json, cantidad = 6, Total = Mis_play)


@app.route('/modificar/<int:id_Playlist>')
def modificar(id_Playlist):
	aux = db.playlist.find_one({"_id":int(id_Playlist)})
	Numeros = [try_int(x) for x in  aux['canciones']]
	canciones_usuario = db.canciones.find({"_id":{"$in":Numeros}})
	canciones_restantes = db.canciones.find({"_id":{"$not":{"$in":Numeros}}})
	canciones_restantes2 = db.canciones.find({"_id":{"$not":{"$in":Numeros}}})
	total = db.canciones.find({"_id":{"$not":{"$in":Numeros}}}).count()
	cant = json.dumps(list(canciones_restantes2))
	categorias = ','.join(aux['categorias'])

	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})

	return render_template('menu_modificar_playlist.html', info = datos, json1 = aux, cate = categorias, json_can1 = canciones_usuario, json_Aux = canciones_restantes, json2 = cant, cantidad = 5, Total = total)


@app.route('/modificada', methods=['POST'])
def modificada(err=None):
	global Usuario_Activo
	file = request.files['imagen']
	Titulo = request.form['titulo']
	Descripcion = request.form['descripcion']
	Categorias = request.form['categorias']
	Canciones = request.form['canciones']
	Identificador = int(request.form['identificador'])
	Temporal = Categorias.replace(' ','')
	Auxiliar_1 = Temporal.split(',')
	Auxiliar_2 = Canciones.split(',')
	Canciones_v = db.canciones.find({}).count() + 1;

	for x in range(1, Canciones_v):
		temporal = db.canciones.find_one({"_id":int(x)})
		Playlist_viejas = temporal["playlists"]
		if int(Identificador) in Playlist_viejas:
			Playlist_viejas.remove(int(Identificador))
		db.canciones.update({"_id":int(x)},{"$set":{'playlists':Playlist_viejas}})

	for x in Auxiliar_2:
		temporal = db.canciones.find_one({"_id":int(x)})
		Playlist_viejas = temporal["playlists"]
		Playlist_viejas.append(Identificador)
		db.canciones.update({"_id":int(x)},{"$set":{'playlists':Playlist_viejas}})

	db.playlist.update({"_id":Identificador},{"$set":{'canciones':Auxiliar_2}})
	db.playlist.update({"_id":Identificador},{"$set":{'titulo':Titulo}})
	db.playlist.update({"_id":Identificador},{"$set":{'descripcion':Descripcion}})
	db.playlist.update({"_id":Identificador},{"$set":{'categorias':Auxiliar_1}})

	Playlist_Actual = db.playlist.find_one({"_id":Identificador})
	filename = secure_filename(file.filename)

	if filename != Playlist_Actual['imagen'] and filename != '':
		ruta_trabajo = os.getcwd()
		os.remove(ruta_trabajo + "/static/imagenes/Usuarios/"+ str(Usuario_Activo) + '/Playlist/' + Playlist_Actual['imagen'])
		UPLOAD_FOLDER = ruta_trabajo +'/static/imagenes/Usuarios/'+ str(Usuario_Activo) + '/Playlist'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		db.playlist.update({"_id":Identificador},{"$set":{'imagen':filename}})

	return redirect(url_for('principal'))


@app.route('/mis_playlist_delete')
def mis_playlist_delete():
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})
	aux = db.playlist.find({'usuario':Usuario_Activo})
	aux2 = db.playlist.find({'usuario':Usuario_Activo})
	Mis_play = db.playlist.find({'usuario':Usuario_Activo}).count()
	Mis_json = json.dumps(list(aux2))
	
	return render_template('eliminar_playlist.html', info = datos, json1 = aux, json2 = Mis_json, cantidad = 6, Total = Mis_play)


@app.route('/delete', methods=['POST'])
def delete():
	global Usuario_Activo
	Elegida = request.form['play']
	temporal = db.playlist.find_one({"_id":int(Elegida)})
	ruta_trabajo = os.getcwd()
	os.remove(ruta_trabajo + "/static/imagenes/Usuarios/"+ str(Usuario_Activo) + '/Playlist/' + temporal['imagen'])
	db.playlist.remove({"_id":int(Elegida)})
	
	return redirect(url_for('principal'))


@app.route('/reproductor/<int:id_Playlist>')
def reproductor(id_Playlist):
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})

	aux = db.playlist.find_one({"_id":int(id_Playlist)})
	Numeros = [try_int(x) for x in  aux['canciones']]
	canciones_usuario = db.canciones.find({"_id":{"$in":Numeros}})
	ciclo = db.canciones.find({"_id":{"$in":Numeros}})
	cuenta= db.canciones.find({"_id":{"$in":Numeros}}).count()
	ytcanc = json.dumps(list(ciclo))
	aux2 = aux["usuario"]
	usr = db.usuarios.find_one({"_id":int(aux2)})
	name = usr["correo"]

	aux3 = db.playlist.find_one({"_id":int(id_Playlist)})
	temp = [try_int(y) for y in  aux3['usuario_like']]
	
	aux4 = db.playlist.find_one({"_id":int(id_Playlist)})
	temp2 = [try_int(y) for y in  aux4['favorito']]

	if x in temp:
		valor = 1
	else:
		valor = 0

	if x in temp2:
		valor2 = 1
	else:
		valor2 = 0

	categorias = ','.join(aux['categorias'])
	tempc = db.comentarios.find({"pl":int(id_Playlist)})
	tc = db.comentarios.find({"pl":int(id_Playlist)}).count()

	return render_template('reproductor.html',info = datos, pl = aux, canc = canciones_usuario, autor = name, json = usr, lista = ytcanc, tot = cuenta, coment = tempc, totcom = tc, val1 = valor, val2 = valor2, cat = categorias)


@app.route('/reproductor_no_sesion/<int:id_Playlist>')
def reproductor_no_sesion(id_Playlist):
	aux = db.playlist.find_one({"_id":int(id_Playlist)})
	Numeros = [try_int(x) for x in  aux['canciones']]
	canciones_usuario = db.canciones.find({"_id":{"$in":Numeros}})
	ciclo = db.canciones.find({"_id":{"$in":Numeros}})
	cuenta= db.canciones.find({"_id":{"$in":Numeros}}).count()
	ytcanc = json.dumps(list(ciclo))
	aux2 = aux["usuario"]
	usr = db.usuarios.find_one({"_id":int(aux2)})
	name = usr["correo"]

	categorias = ','.join(aux['categorias'])
	tempc = db.comentarios.find({"pl":int(id_Playlist)})
	tc = db.comentarios.find({"pl":int(id_Playlist)}).count()
	return render_template('reproductor-noSesion.html', pl = aux, canc = canciones_usuario, autor = name, json = usr, lista = ytcanc, tot = cuenta, coment = tempc, totcom = tc, cat = categorias)


@app.route('/Perfil')
def Perfil():
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})

	aux = db.playlist.find({'usuario':Usuario_Activo})
	aux2 = db.playlist.find({'usuario':Usuario_Activo})
	Mis_play = db.playlist.find({'usuario':Usuario_Activo}).count()
	Mis_json = json.dumps(list(aux2))
	
	listaf = []
	listaf.append(x);
	aux3 = db.playlist.find({'favorito':{'$in':listaf}})
	aux4 = db.playlist.find({'favorito':{'$in':listaf}})
	Mis_play2 = db.playlist.find({'favorito':{'$in':listaf}}).count()
	Mis_json2 = json.dumps(list(aux3))
	
	return render_template('perfil.html', info = datos, json1 = aux, json2 = Mis_json, cantidad = 6, Total = Mis_play, jsonf1 = aux4, jsonf2 = Mis_json2, Totalf = Mis_play2)


@app.route('/Pre_Perfil')
def Pre_Perfil():
	global Usuario_Activo
	x = int(Usuario_Activo)
	datos = db.usuarios.find_one({"_id": x})

	Playlist = db.playlist.find().sort([("tlikes",-1)])
	Playlist_aux = db.playlist.find().sort([("tlikes",-1)])
	Playlist_Totales = db.playlist.find().count()
	Mis_json = json.dumps(list(Playlist_aux))

	return render_template('perfil-EditarD.html', info = datos)


@app.route('/Editar_Perfil', methods=['POST'])
def Editar_Perfil():
	global Usuario_Activo
	x = int(Usuario_Activo)
	user = db.usuarios.find_one({"_id": x})
	old = user["contrasena"]
	old_f = user["imagen"]

	nombre = request.form['nombre']
	last = request.form['apellido']
	usr = request.form['user']
	mail = request.form['correo']
	city = request.form['ciudad']
	country = request.form['pais']
	born = request.form['nacimiento']
	likes = request.form['interes']

	db.usuarios.update({"_id":x},{"$set":{'contrasena':old, 'name':nombre, 'imagen':old_f, 'apellido':last, 'usuario':usr, 'correo':mail, 'ciudad':city, 'pais':country, 'nacimiento':born, 'intereses':likes}})

	return redirect(url_for('principal'))

@app.route('/New_Pass', methods=['POST'])
def New_Pass():
	global Usuario_Activo
	x = int(Usuario_Activo)
	
	user = db.usuarios.find_one({"_id": x})
	old = user["contrasena"]

	pass1 = request.form['new1']
	pass2 = request.form['new2']

	if pass1 == pass2:
		db.usuarios.update({'contrasena':old},{"$set":{'contrasena':pass1}})
		return redirect(url_for('principal'))
	else:
		return redirect(url_for('Perfil'))


@app.route('/New_Pic', methods=['POST'])
def New_Pic():
	global Usuario_Activo
	x = int(Usuario_Activo)

	user = db.usuarios.find_one({"_id": x})
	old = user["imagen"]
	file = request.files['imagen']
	filename = secure_filename(file.filename)
	print(filename)
	if filename != old and filename != '':
		ruta_trabajo = os.getcwd()
		UPLOAD_FOLDER = 'static/imagenes/Perfiles'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		db.usuarios.update({'imagen':old},{"$set":{'imagen':filename}})

	return redirect(url_for('Perfil'))

@app.route('/Comentar/<int:id_Playlist>', methods=['POST'])
def Comentar(id_Playlist):

	global Usuario_Activo
	user_id = int(Usuario_Activo)
	user = db.usuarios.find_one({"_id":user_id})
	img = user["imagen"]
	nomb = user["correo"]

	pl_id = int(id_Playlist)
	texto = request.form['comentario']
	total = db.comentarios.find({}).count()+1

	db.comentarios.insert({"_id":total, "user":user_id, "name":nomb, "pic":img, "pl":pl_id, "comentario":texto })

	return redirect(url_for('reproductor', id_Playlist = pl_id))

@app.route('/dar_fav', methods=['PUT'])
def dar_fav():
	id_pl = request.args.get('id')

	global Usuario_Activo
	user_id = int(Usuario_Activo)

	PL = db.playlist.find_one({"_id": int(id_pl)})
	lista = PL["favorito"]
	if len(lista) > 0:
		if user_id in lista:
			lista.remove(user_id)
		else:
			lista.append(user_id)
	else:
		lista.append(user_id)

	db.playlist.update({"_id":int(id_pl)},{"$set":{"favorito":lista}})
	
	return "peticion satisfactoria"

@app.route('/me_gusta', methods=['PUT'])
def me_gusta():
	id_pl = request.args.get('id')

	global Usuario_Activo
	user_id = int(Usuario_Activo)

	PL = db.playlist.find_one({"_id":int(id_pl)})
	lista = PL["usuario_like"]
	total = PL["me_gusta"]

	if len(lista) > 0:
		if user_id in lista:
			total = total - 1;
			lista.remove(user_id)
		else:
			total = total + 1;
			lista.append(user_id)
	else:
		total = total + 1;
		lista.append(user_id)
	
	db.playlist.update({"_id":int(id_pl)},{"$set":{"me_gusta":total,"usuario_like":lista}})

	return "peticion satisfactoria"

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0') # direccion ip movil 192.168.0.101:5000