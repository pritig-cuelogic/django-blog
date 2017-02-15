$(function() {
         
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
  $("#id_tags")
        .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
        
      })
  .autocomplete({
            source: function( request, response ) {
                $.getJSON( "/blog/get_tags", {
                    term: extractLast( request.term )
                }, response );
            },
            search: function() {
            var term = extractLast( this.value );
            if ( term.length < 1 ) {
                return false;
            }
            },
            focus: function() {
            return false;
            },
            select: function( event, ui ) {
                var terms = split( this.value );
                terms.pop();
                terms.push( ui.item.value );
                terms.push( "" );
                this.value = terms.join( ", " );
                tags_id_arr.push(ui.item.id)
                return false;
            }
    });
});