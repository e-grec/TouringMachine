/* Script for CSCE 470 search engine
 *
 */
var tweet_template = _.template($('#tweet_template').html());
var result_template = _.template($('#result_template').html());
var alert_template = _.template($('#alert_template').html());
var city_template = _.template($('#city_template').html());
var city_ranking_template = _.template($('#city_ranking_template').html());
var similar_artist_ranking_template = _.template($('#similar_artist_ranking_template').html());

$('#bandsearch form').submit(function(ev) {
    var q = $(this).find('input[name=query]').val();
    ajax_search(q);
    return false;
});


function ajax_search(q) {
  $.ajax('/bandsearch',{
      data:{q:q},
      timeout:15000,
      success: function(data) {
        var result_div = $('#bandsearch .results');

        result_div.empty();
        result_div.show();
        result_div.append($(result_template(data)));
        var city_divs = _.map(data.cities, city_ranking_template);
		result_div.append("<h3>Top Cities for " + q + ":</h3>");
        result_div.append(city_divs.join(''));

	var similar_artists = similar_artist_ranking_template(data.cities[0]);
	result_div.append(similar_artists);


//	var city_result_div = $('#bandsearch .results #city_results');
//	var similar_artist_div = $('#bandsearch .results .similar_artists');

//	city_result_div.empty();
//	city_result_div.show();
//	similar_artist_div.empty();
//	similar_artist_div.show();
	

//	city_result_div.append(city_divs.join('')); 
//	similar_artist_div.append(similar_artists);
	
      },
      error: function(jqXHR,textStatus,errorThrown) {
        var error;
        if(textStatus=='error') {
          if(jqXHR.status==0)
            error = "Could not connect to server. Try running ./serve.py.";
          else
            error = jqXHR.status+" : "+errorThrown;
        } else {
          error = textStatus;
        }

        var alert = alert_template({error:error});
        $('#bandsearch form').after(alert);
        $('#bandsearch .results').hide();
      },
      dataType: 'json',

  });
}

