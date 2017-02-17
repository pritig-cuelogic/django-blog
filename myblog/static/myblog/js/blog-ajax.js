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
        			
              }
        		else{
					      $("#hiddenunlike"+id_num).val(data);
        		}
            var like_c = $("#hiddenlike"+id_num).val();
            var unlike_c = $("#hiddenunlike"+id_num).val();
            var final_val = like_c - unlike_c;
            final_val >0 ?final_val = final_val :final_val =0;
            $("#liketext"+id_num).val(final_val);
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

