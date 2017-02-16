function manageCommentLike(id){
       var like_val = 0;
       var id_num = id.replace( /^\D+/g, '');
       (id == 'like'+id_num)?like_val = 1: like_val = 2;
       	
       $.getJSON( "/blog/manage_like", {
                    cat_id: id_num,
                    like_val: like_val
        }, function(data,status,xhr){
        	if(status == 'success'){
        		if(id == 'like'+id_num){
        			$("#like"+id_num).hide();
       	            $("#unlike"+id_num).show();
            	}
        		else{
					$("#like"+id_num).show();
       	   			$("#unlike"+id_num).hide();
        		}
        	}
         
        } );
}