
var currentPage = 1;
var nextPage = function() { currentPage += 1; getPage(currentPage) };
var lastPage = function() { if ( currentPage > 1 ) { currentPage -= 1; getPage(currentPage) } };
var getPage = function(page) {
	jQuery('#queries-table tbody').empty();
	var url = document.URL + '/_page/'+page.toString()
	var response = jQuery.getJSON( url, function(data) {
		data.queries.forEach( function (value){
			var row = jQuery('<tr></tr>');
			var q = value['query'];
			row.append('<td>'+value['qtime']+'</td>');
			row.append('<td><span class="action query" data-query="'+q+'">...'+q.substring(q.length-85, q.length)+'</a></td>');
			jQuery('#queries-table tbody').append(row);
		    });
	    });
};


getPage(1);

jQuery(document).ready( function() {

	jQuery('#queries').slideDown();

	jQuery('#back').on( 'click', function(e) {
		lastPage();
		e.stopPropagation();
	});

	jQuery('#more').on( 'click', function(e) {
		nextPage();
		e.stopPropagation();
	});

	jQuery('#return').on( 'click', function() {
		jQuery('#query').slideUp( 50, function() { jQuery('#queries').slideDown(); } );
	});

	jQuery('#queries-table').on( 'click', 'tr td span.query', function() {
		jQuery.post(document.URL+'/_query/', { 'query': jQuery(this).data('query') }, function(jsonString, status) {
			var data = jQuery.parseJSON(jsonString);
			jQuery('#query h4').text(data.query);
			jQuery('#query-table tbody').empty();
			data.instances.forEach( function(datum) {
				var row = jQuery('<tr></tr>');
				row.append(jQuery('<td>'+(new Date(datum.timestamp.$date)).toISOString()+'</td>'));
				row.append(jQuery('<td>'+datum.qtime+'</td>'));
				row.append(jQuery('<td>'+datum.hits+'</td>'));
				jQuery('#query-table tbody').append(row);
			    });
			jQuery('#queries').slideUp( 50, function() { jQuery('#query').slideDown(); } );
		    } );
	});

});