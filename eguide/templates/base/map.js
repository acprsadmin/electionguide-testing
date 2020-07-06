// Detect
// ------------------------------------------------------
var supportsCssTransitions = (function(style)
{
    var prefixes = ['Webkit','Moz','Ms','O'];
    for( var i=0, l=prefixes.length; i < l; i++ ) {
        if( typeof style[prefixes[i] + 'Transition'] !== 'undefined') {
            return true;
        }
    }
    return false;
})(document.createElement('div').style);

// Map
// ------------------------------------------------------
if( $('#map').size() > 0 )
{
    var Popup = {
        Show: function(geography, data, element, e)
        {
            e.stopPropagation();

            console.log('hi', e.clientY);

            var el =
            '<a href="' + data.url + '"class="popup-card"> \
                <span class="country">' + geography.properties.name + '</span>\
                <span>' +  data.election + '</span>\
                <span><em>Date:</em> ' +  data.date + '</span>\
            </a>';
            
            var $el = $(el).css({
                top: e.clientY - 10,
                left: e.clientX
            });

            if( !supportsCssTransitions ) $el.addClass('compatible');
            
            Popup.Hide();
            $('body').append($el);
        },

        Hide: function()
        {
            $('body .popup-card').remove();
        }
    };

    var dataMap = new Datamap(
    {
        element         : document.getElementById('map'),
        scope           : 'world',
        projection      : 'mercator',
        geographyConfig : {
            highlightBorderColor : '#fff',
            highlightBorderWidth : 1,
            highlightFillColor   : '#f75455',
            popupOnHover         : false
        },
        fills : {
            'GRAY1'     : '#7e8b8d',
            defaultFill : '#c2c2c2'
        },
        data : {
        	{% for item in election%}
			    {% if item.country.alpha3 %}
			        '{{item.country.alpha3}}'	: {
			            fillKey    	: 'GRAY1',
			            election 	: '{% if item.institution.name %}Election for {{item.institution.name}}{% else %}Referendum{% endif %}',
			            date    	: '{{item.date}}',
			            url        	: '{% url "election" item.id%}'
			        }{% if not forloop.last %},{% endif %}
			    {% endif %}
			{% endfor %}
        },

        done: function(datamap)
        {
            datamap.svg.selectAll('.datamaps-subunit').on('click', function(geography) {
                Popup.Show(geography, datamap.options.data[geography.id], this, d3.event);
            });
        }
    });

    $('body').on('click', function(e){
        Popup.Hide();
    })
    .on('click', '.datamaps-subunit,.popup-card', function(e){
        e.stopPropagation();
    });
}