$(document).ready(function () {
    var CSRF_TOKEN = '{{ csrf_token }}';
    function filter(e) {
        e.stopPropagation();
        e.stopImmediatePropagation();
        let filter = $('#filter-form').serializeArray();
        let request_data = {};
        let loading = '<div id="loading"><p><img src="/media/icons/ajax-loader.gif" alt="Loading..."></p></div>'
        let result_msg = '<div id="result-msg"></div>'

        $(filter).each(function(index, obj){
            request_data[obj.name] = obj.value
        });
        console.log(request_data);
        $.ajax({
            url: '/property?' + $.param(request_data),
            type: 'GET',
            beforeSend: function() {
                $('#result-msg').remove();
                $('.property-overview').html('').prepend(loading);
                $('#filter_props').prop('disabled', true)
            },
            success: function (resp) {
                let newHTML = resp.data.map(function(d) {
                    return `<a href="/property/${d.id}" class="link-to-property">
                                <div class="card property">
                                    <img class="property-img" src="${d.firstImage}"/>
                                    <div class="card-body">  
                                        <div id="property-name-address">
                                            <div id="property-name">  
                                                <h5 class="card-title">${d.name}</h5>
                                            </div>
                                            <div id="property-address">
                                                <p>${d.address.city}, ${d.address.country}</p>
                                            </div>
                                        </div>
                                        <div id="property-price-info">
                                            <p class="card-subtitle mb-2">Price: ${d.price} $ <br>
                                            Size: ${d.squareMeters}m<sup>2</sup>, ${d.nrBedrooms} bedrooms, ${d.nrBathrooms} bathrooms</p>
                                        </div>
                                    </div>
                                </div>
                            </a>`
                });
                if(newHTML === undefined || newHTML.length === 0) {
                    $('.property-overview').append(result_msg)
                    $('#result-msg').html('<h3>No results found!</h3>')
                }
                else {
                    $('.property-overview').append(newHTML.join(''));
                    $('#search-box').val('');
                }
            },
            complete: function(){
                $('#loading').remove();
                $('#filter_props').prop('disabled', false);
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
                $('#filter_props').prop('disabled', false);
            },
        });
    };
    $('#filter_props').on('click', function (e) {
        e.preventDefault();
        filter(e);
    });
    $('#search-box').on('keypress', function (e) {
        if(e.which == 13) {
            filter(e);
        }
    });
    /*
    let p1 = '<input id="purchase-continue" class="btn btn-primary pull-right" type="button" value="Continue">'
    let p2 = '<input id="purchase-confirm" class="btn btn-primary pull-right" type="submit" value="Purchase Property">'
    $('#purchase-cancel').on('click', function (e) {
        console.log('Cancel')
        $('.purchase-property-form :input').prop('disabled', false);
        if($('#purchase-cancel').val() === 'Cancel') {
            let url_parts = $(location).attr('href').split("/");
            let prop_id = url_parts[url_parts.length-1];
            window.location.replace('/property/' + prop_id);
        }
        $('#purchase-cancel').val( 'Cancel' );
        //$('#purchase-continue').replaceWith(p1);
        $('#purchase-continue').prop('style', '')
        $('#purchase-confirm').prop('style', 'display: none')
    });
    $('#purchase-continue').on('click', function (e) {
        console.log('Continue')
        $('.purchase-property-form :input').prop('disabled', true);
        $('#purchase-cancel').prop('disabled', false).val( 'Edit Information' );
        //$('#purchase-continue').replaceWith(p2);
        $('#purchase-continue').prop('disabled', false).prop('style', 'display: none')
        $('#purchase-confirm').prop('disabled', false).prop('style', '')
    });
    */
});
