$(document).ready(function () {
    //
    //
    //Variables
    //
    //
    let loading = '<div id="loading"><p><img src="/media/icons/ajax-loader.gif" alt="Loading..."></p></div>';
    let result_msg = '<div id="result-msg"></div>';

    let url_parts = $(location).attr('href').split("/");

    function propertyHTML(d) {
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
    }
    //
    //
    //Loading the initial property list.
    //
    //
    if (window.location.pathname === '/property/') {
        $.ajax({
            url: '/property/',
            type: 'GET',
            cache: false,
            beforeSend: function() {
                $('#result-msg').remove();
                $('.property-overview').html('').prepend(loading);
                $('#filter_props').prop('disabled', true);
            },
            success: function (resp) {
                let newHTML = resp.data.map(function(d) {
                    return propertyHTML(d);
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
    }
    //
    //
    //Filtering function
    //
    //
    function filter(e) {
        e.stopPropagation();
        e.stopImmediatePropagation();
        let filter = $('#filter-form').serializeArray();
        let request_data = {};
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
                    return propertyHTML(d)
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
    }
    $('#filter_props').on('click', function (e) {
        e.preventDefault();
        filter(e);
    });
    $('#search-box').on('keypress', function (e) {
        if(e.which === 13) {
            filter(e);
        }
    });
    function purchaseStep1() {
        $('#purchase-paragraph').replaceWith('<h3 id="purchase-paragraph">Please fill out the form below</h3>');
        $('.purchase-property-form :input').prop('disabled', false);
        $('#purchase-cancel').prop('style', '');
        $('#purchase-continue').prop('style', '');
        $('#purchase-edit').prop('style', 'display: none');
        $('#purchase-confirm').prop('style', 'display: none');
    }
    function purchasestep2() {
        $('#purchase-paragraph').replaceWith('<h3 id="purchase-paragraph">Is this information correct?</h3>');
        $('.purchase-property-form :input').prop('disabled', true);
        $('#purchase-cancel').prop('disabled', false).prop('style', 'display: none');
        $('#purchase-continue').prop('disabled', false).prop('style', 'display: none');
        $('#purchase-edit').prop('disabled', false).prop('style', '');
        $('#purchase-confirm').prop('disabled', false).prop('style', '');
    }
    if (url_parts[url_parts.length-2] === 'purchase') {
        purchaseStep1();
    }
    $('#purchase-cancel').on('click', function (e) {
        window.location.replace('/property/' + url_parts[url_parts.length-1]);
    });
    $('#purchase-continue').on('click', function (e) {
        purchasestep2();
    });
    $('#purchase-edit, #purchase-confirm').on('click', function (e) {
        purchaseStep1();
    });
    $('#id_payment-cardNumber, #id_payment-cardCVC, #id_payment-cardExpiryMonth, #id_payment-cardExpiryYear, #id_profile-phone').on('keypress', function (e) {
        if( 48 > e.which || e.which > 57 ) {
            e.preventDefault();
        }
    });
});
