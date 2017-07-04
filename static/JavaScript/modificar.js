function borrar(id){
	var parent=document.getElementById("lista");
	var hijo=document.getElementById(id);
	var texto=$("#" + id).text(); 
	parent.removeChild(hijo);
				
	var parent=document.getElementById("lista-b");
				
	var list =document.createElement('li');
	list.setAttribute("id",(id));

	var s=document.createElement('span');
	s.setAttribute("class",("glyphicon glyphicon-music"));

	list.appendChild(s);

	var nombre=document.createTextNode(texto);
	list.appendChild(nombre);

	var link=document.createElement('a');
	link.setAttribute("class",("x"));
	link.setAttribute("id",(id));
	link.setAttribute("onclick","(agregar(this.id))");

	var i=document.createElement('i');
	i.setAttribute("class",("fa fa-plus-circle"));

	link.appendChild(i);

	list.appendChild(link);

	parent.appendChild(list);

}

function borrar2(dir2){
	var parent=document.getElementById("lista-b");
	var hijo=document.getElementById(dir2); 
	parent.removeChild(hijo);

}

function agregar(dir) {

	var padre=document.getElementById("lista-b");
	var hijo=document.getElementById(dir); 
	var texto=$("#" + dir).text();

	borrar2(dir);

	var parent=document.getElementById("lista");

	var list =document.createElement('li');
	list.setAttribute("id",(dir));

	var s=document.createElement('span');
	s.setAttribute("class",("glyphicon glyphicon-music"));

	list.appendChild(s);

	var nombre=document.createTextNode(texto);
	list.appendChild(nombre);

	var link=document.createElement('a');
	link.setAttribute("class",("x"));
	link.setAttribute("id",(dir));
	link.setAttribute("onclick","(borrar(this.id))");

	var i=document.createElement('i');
	i.setAttribute("class",("fa fa-times"));

	link.appendChild(i);

	list.appendChild(link);

	parent.appendChild(list);
}

var cant = 5;

function cargar(k, l) {
	var total = parseInt(l);
	var MiJSON = jQuery.parseJSON(k);
	var Subidas = 0;
	var Max_cant;
	if (total >= cant + 5) {
		Max_cant = cant + 5;
	}else{
		Max_cant = total;
	}
	for(var j = cant; j < Max_cant; j++){		
		var parent=document.getElementById("lista-b");
				
		var list =document.createElement('li');
		list.setAttribute("id",(MiJSON[j]._id));

		var s=document.createElement('span');
		s.setAttribute("class",("glyphicon glyphicon-music"));

		list.appendChild(s);

		var nombre=document.createTextNode(' '+ MiJSON[j].titulo + ' - ' + MiJSON[j].artista);
		list.appendChild(nombre);

		var link=document.createElement('a');
		link.setAttribute("class",("x"));
		link.setAttribute("id",(MiJSON[j]._id));
		link.setAttribute("onclick","(agregar(this.id))");

		var i=document.createElement('i');
		i.setAttribute("class",("fa fa-plus-circle"));

		link.appendChild(i);

		list.appendChild(link);

		parent.appendChild(list);
		Subidas++;
	};
	cant = cant + Subidas;
	
	if(cant == total){
		var x = document.getElementById("b-cargar");
        x.setAttribute("style",("display:none;"));
	}
}
	
