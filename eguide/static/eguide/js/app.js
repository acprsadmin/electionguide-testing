function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

$(document).ready(function()
{
    // Tooltip
    // ------------------------------------------------------
    $("[data-title]").tooltip({
        placement: 'top'
    });

    // Tabs
    // ------------------------------------------------------
    $('.tabs a').on('click', function(e)
    {
        e.preventDefault();

        var self = $(this)
          , prnt = self.parents('.tab-container')
          , tabs = self.parent().find('a')
          , id   = self.attr('href');

        tabs.removeClass('active');
        self.addClass('active');

        prnt.find('.tab-content').removeClass('active');
        prnt.find(id).addClass('active');
    });

    // Carousel
    // ------------------------------------------------------
    $('#myCarousel').carousel({
        pause    : 'hover',
        interval : 8000
    });

    $('#sideCarousel').carousel({
        pause    : 'hover',
        interval : 5000
    });

    // Search
    // ------------------------------------------------------
    if( $('aside .search').length > 0 )
    {
        var fields = ['inst', 'cont', 'yr']
          , $form  = $('aside .search');

        for(i = 0; i < fields.length; i++){
            var value  = getURLParameter(fields[i]).replace(/\+/g, ' ')
              , select = $form.find('select[name="'+fields[i]+'"]');

            if( typeof value == 'string' ){
                select.find('option').removeAttr('selected');
                select.find('option').filter(function() {
                    if( jQuery.trim($(this).text()) == jQuery.trim(value) ){
                        $(this).attr('selected', 'selected');
                        select.trigger('change');
                    }
                });
            }
        }
    }
    
    $('select[name="yr"]').change(function() {
    	var action = '';
    	if($(this).children(':selected').text() == 'upcoming') action = 'upcoming/';
    	$('aside .search').attr('action', '/elections/' + action);
    });
    
    // Select Box
    // ------------------------------------------------------
    $("aside .search select").selectpicker({
        style: 'btn-inverse',
        // menuStyle: 'dropdown-inverse',
        width: '100%'
    });
    
    $(function(){
		$('#menu').slicknav();
	});

});