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
                <span><em>Capital:</em> ' +  data.capital + '</span>\
                <span><em>Poptulation:</em> ' +  data.population.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + '</span>\
                <span><em>Currency:</em> ' +  data.currency + '</span>\
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
            popupOnHover         : true
        },
        fills : {
            'GRAY1'     : '#7e8b8d',
            defaultFill : '#c2c2c2'
        },
        data : {
            'IND': {
                fillKey    : 'GRAY1',
                population : 1210193422,
                capital    : 'New Dehli',
                currency   : 'Indian Rupee (INR)',
                url        : '/somewhere.html'
            },
            'GBR': {
                fillKey    : 'GRAY1',
                population : 63181775,
                capital    : 'London',
                currency   : 'Pound Sterling (GBP)',
                url        : '/somewhere.html'
            },
            'FRA': {
                fillKey    : 'GRAY1',
                population : 63460000,
                capital    : 'Paris',
                currency   : 'Euro (EUR)',
                url        : '/somewhere.html'
            },
            'USA': {
                fillKey    : 'GRAY1',
                population : 316424000,
                capital    : 'Washington D.C',
                currency   : 'US Dollars (USD)',
                url        : '/somewhere.html'
            },
            'IRN': {
                fillKey    : 'GRAY1',
                population : 77176930,
                capital    : 'Tehran',
                currency   : 'Iranian Rails (IRR)',
                url        : '/somewhere.html'
            }
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