function manageCommentLike(id){
       var like_val = 0;
       var id_num = getNumericVal(id) ;
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

function deleteComment(id){
  var id_num = getNumericVal(id);
  $.getJSON( "/blog/delete_comment", {
          cat_id: id_num
        },function(data, status){
            
              document.getElementById("comment"+id_num).style.visibility='hidden'
           
        });
}

function getNumericVal(id){
  return id.replace( /^\D+/g, '');
}