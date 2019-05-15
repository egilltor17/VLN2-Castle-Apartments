$(document).ready(function () {
    //
    //
    //Variables
    //
    //
    let loading = '<div id="loading"><p><img src="/media/icons/ajax-loader.gif" alt="Loading..."></p></div>'
    let result_msg = '<div id="result-msg"></div>'
    let url_parts = $(location).attr('href').split("/");
    let default_option = '<option value="">All</option>'
    // $('#municipality_dropd').prop('disabled', true)
    // $('#city_dropd').prop('disabled', true)
    // $('#postcode_dropd').prop('disabled', true)

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
            data: 'initial_filter',
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
    //Conditional filters
    //
    //
    //Countries->Municipalities
    $('#country_dropd').change(function() {
        let selected_country = $('#country_dropd').val();
        let selected_city = $('#city_dropd').val();
        if(selected_country === ""){
            $('#municipality_dropd').html(default_option)
            $('#city_dropd').html(default_option)
            $('#postcode_dropd').html(default_option)
        }
        else{
                    $.ajax({
            type: 'GET',
            data: {
                enable_municipalities: '',
                country: selected_country,
                city: selected_city
            },
            url: '/property',
            beforeSend: function() {
                $('#filter_props').prop('disabled', true);
                $('#municipality_dropd').find('option').not(':first').remove();
                $('#city_dropd').find('option').not(':first').remove();
                $('#postcode_dropd').find('option').not(':first').remove();


            },
            success: function(resp) {
                let municiHTML = ``;
                let cityHTML = ``;
                for (let i = 0; i < resp.data.length; i++) {
                    if(resp.data[i].municipalities == null){
                        cityHTML += `<option value = "${resp.data[i].cities}">${resp.data[i].cities}</option>`
                    }
                    else{
                        municiHTML += `<option value = "${resp.data[i].municipalities}">${resp.data[i].municipalities}</option>`

                    }

                }
                $('#municipality_dropd').append(municiHTML);
                $('#city_dropd').append(cityHTML);

            },
            complete: function(){
                $('#filter_props').prop('disabled', false);

            }
        })
        }

    });
    //Municipalities->Cities
    $('#municipality_dropd').change(function() {
        let selected_municipality = $('#municipality_dropd').val();
        if(selected_municipality === ""){
            $('#city_dropd').html(default_option)
            $('#postcode_dropd').html(default_option)
        }

        else{
            $.ajax({
            type: 'GET',
            data: {
                enable_cities: '',
                municipality: selected_municipality,
            },
            url: '/property',
            beforeSend: function() {
                $('#filter_props').prop('disabled', true);
                $('#city_dropd').find('option').not(':first').remove();
                $('#postcode_dropd').find('option').not(':first').remove();

            },
            success: function(resp) {
                let newHTML = ``;
                for (let i = 0; i < resp.data.length; i++) {
                    newHTML += `<option value = "${resp.data[i].cities}">${resp.data[i].cities}</option>`
                }
                $('#city_dropd').append(newHTML);
            },
            complete: function(){
                $('#filter_props').prop('disabled', false);

            }
        })
        }
    });
    //Cities->Postcodes
    $('#city_dropd').change(function() {
        let selected_city = $('#city_dropd').val();
        if(selected_city === ""){
            $('#postcode_dropd').html(default_option)
        }
        else {
            $.ajax({
            type: 'GET',
            data: {
                enable_postcodes: '',
                city: selected_city,
            },
            url: '/property',
            beforeSend: function() {
                $('#filter_props').prop('disabled', true);

            },
            success: function(resp) {
                let newHTML = ``;
                for (let i = 0; i < resp.data.length; i++) {
                    newHTML += `<option value = "${resp.data[i].postcodes}">${resp.data[i].postcodes}</option>`

                }
                $('#postcode_dropd').append(newHTML);
            },
            complete: function(){
                $('#filter_props').prop('disabled', false);

            }
        })
        }
    });
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
                console.log(resp)
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
    if (url_parts[url_parts.length-2] === 'purchase') {
        $('#purchase-cancel').prop('style', '')
        $('#purchase-continue').prop('style', '')
        $('#purchase-edit').prop('style', 'display: none')
        $('#purchase-confirm').prop('style', 'display: none')
    }
    $('#purchase-cancel').on('click', function (e) {
        let prop_id = url_parts[url_parts.length-1];
        window.location.replace('/property/' + prop_id);
    });
    $('#purchase-continue').on('click', function (e) {
        $('.purchase-property-form :input').prop('disabled', true);
        $('#purchase-cancel').prop('disabled', false).prop('style', 'display: none');
        $('#purchase-continue').prop('disabled', false).prop('style', 'display: none')
        $('#purchase-edit').prop('disabled', false).prop('style', '')
        $('#purchase-confirm').prop('disabled', false).prop('style', '')
    });
    $('#purchase-edit, #purchase-confirm').on('click', function (e) {
        $('.purchase-property-form :input').prop('disabled', false);
        $('#purchase-cancel').prop('style', '');
        $('#purchase-continue').prop('style', '')
        $('#purchase-edit').prop('style', 'display: none')
        $('#purchase-confirm').prop('style', 'display: none')
    });
});
