function manageCommentLike(id){
       var like_val = 0;
       var count;
       var id_num = getNumericVal(id) ;
       if (id == 'like'+id_num) {
             like_val = 1 ;
             count = $("#hiddenlike"+id_num).val();
             
         }
         else {
          like_val = 2 ;
          count = $("#hiddenunlike"+id_num).val();
         } 
       	
       $.getJSON( "/blog/manage_like", {
                    cat_id: id_num,
                    like_val: like_val,
                    like_unlike_count: count
        }, function(data,status,xhr){
        	if(status == 'success'){
        		if(id == 'like'+id_num){
              $("#hiddenlike"+id_num).val(data);
        			$("#like"+id_num).hide();
       	      $("#unlike"+id_num).show();
                          	}
        		else{
					      $("#like"+id_num).show();
       	   			$("#unlike"+id_num).hide();
                $("#hiddenunlike"+id_num).val(data);
        		}
            $("#liketext"+id_num).val(data);
        	}
         
        } );
}

function deleteComment(id){
  var id_num = getNumericVal(id);
  $.getJSON( "/blog/delete_comment", {
          cat_id: id_num
        },function(data, status,xhr){
              $("#comment"+id_num).hide(); 
           
        });
}

function getNumericVal(id){
  return id.replace( /^\D+/g, '');
}

