function favorito(id){
		$(document).ready(function(){
					$.ajax({
						type:"PUT" ,
						url: '/dar_fav?id='+id,
					  	error: function (xhr, ajaxOptions, thrownError) {
					        alert(xhr.status);
					        alert(thrownError);
					        alert(ajaxOptions);   
					    },
						success: function(){
							console.log("Fav satisfactorio");
						}
					});
		});
}

function like(id){
		$(document).ready(function(){
			$.ajax({
				type:"PUT" ,
				url: '/me_gusta?id='+id,
				error: function (xhr, ajaxOptions, thrownError) {
					alert(xhr.status);
					alert(thrownError);
					alert(ajaxOptions);       
				},
				success: function(){
					console.log("Like satisfactorio");
				}
			});
		});
}