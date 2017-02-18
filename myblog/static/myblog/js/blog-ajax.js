function manageCommentLike(id, user_id, post_id){
  
  var id_num = getNumericVal(id);
  var like_cnt = 0;
  var like_unlike_val = 0;
  var set_likecnt;
  if(id == 'unlike'+id_num){
      like_cnt = 1;
      like_unlike_val =1;
  }
  $.getJSON( "/blog/manage_like", {
                    cmnt_id: id_num,
                    like_cnt: like_cnt,
                    like_unlike_val: like_unlike_val,
                    post_id: post_id
        }, function(data,status,xhr){
          set_likecnt = $("#likecnt"+id_num).val();
          set_likecnt = parseInt(set_likecnt); 
          if(data == 'success'){
            if(id == 'unlike'+id_num){
              document.getElementById("like"+id_num).style.display = "block";
              document.getElementById("unlike"+id_num).style.display = "none";
              $("#likecnt"+id_num).val(set_likecnt+1);
            }
            else{
              document.getElementById("like"+id_num).style.display = "none";
              document.getElementById("unlike"+id_num).style.display = "block";
              set_likecnt = set_likecnt-1;
              set_likecnt>0? set_likecnt=set_likecnt : set_likecnt=0;
              $("#likecnt"+id_num).val(set_likecnt);
            }
          }
        })

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

