
var Paginator = {
    currentPage : 1,
    updateTable: function(page) {
	jQuery('tbody').empty();
	var response = jQuery.getJSON( document.URL + '/_page/1', function(data) {
		data.queries.forEach( function (value){
			var row = jQuery('<tr></tr>');
			row.append('<td>'+value['qtime']+'</td>');
			row.append('<td>'+value['query']+'</td>');
			row.append('<td>'+value['hits']+'</td>');
			jQuery('tbody').append(row);
		    });
	    });
	this.currentPage = page
    }
}



jQuery(document).ready( function() {

	Paginator.updateTable(1);

	jQuery('#back').on( 'click', function() {
		if ( Paginator.currentPage > 1 ) {
		    Paginator.updateTable(Paginator.currentPage - 1)
		}
	});

	jQuery('#more').on( 'click', function() {
	    Paginator.updateTable(Paginator.currentPage + 1)
	});
});