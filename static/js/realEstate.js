$(document).ready(function () {
    //
    //
    //Variables
    //
    //
    let search_box = $('#search-box');
    let country_dropdown = $('#country_dropd');
    let municipality_dropdown = $('#municipality_dropd');
    let city_dropdown = $('#city_dropd');
    let postcode_dropdown = $('#postcode_dropd');
    let filter_button = $('#filter_props');
    let property_overview = $('.property-overview');
    let msg_area = $('#msg-area');
    let loading_elem = $('#loading');
    let result_elem = $('#result');
    msg_area.append(loading_elem);
    msg_area.append(result_elem);
    let url_parts = $(location).attr('href').split("/");

    function disableInput() {
        country_dropdown.prop('disabled', true);
        municipality_dropdown.prop('disabled', true);
        city_dropdown.prop('disabled', true);
        postcode_dropdown.prop('disabled', true);
        filter_button.prop('disabled', true);
    }

    function enableInput() {
        country_dropdown.prop('disabled', false);
        municipality_dropdown.prop('disabled', false);
        city_dropdown.prop('disabled', false);
        postcode_dropdown.prop('disabled', false);
        filter_button.prop('disabled', false);
    }
    function showElem(elem){
        elem.removeClass('hidden')
    }
    function hideElem(elem){
        elem.addClass('hidden')
    }
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
                                <p>Size: ${d.squareMeters}m<sup>2</sup>, ${d.type}, ${d.nrBedrooms} bedrooms, ${d.nrBathrooms} bathrooms</p>
                                <p class="card-subtitle mb-2">Price: ${d.price} $</p>
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
            beforeSend: function () {
                property_overview.html('');
                result_elem.html('');
                showElem(loading_elem);
                disableInput();
            },
            success: function (resp) {
                let newHTML = resp.data.map(function (d) {
                    return propertyHTML(d);
                });
                if (newHTML === undefined || newHTML.length === 0) {
                    msg_area.append(showElem(result_elem.html('<h3>No results found!</h3>')));

                } else {
                    property_overview.append(newHTML.join(''));
                    search_box.val('');
                }
            },
            complete: function () {
                hideElem(loading_elem);
                enableInput();
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                hideElem(loading_elem);
                console.error(error);
                enableInput();
            },
        });
    }
    //
    //
    //Conditional filters
    //
    //
    //Countries->Municipalities
    country_dropdown.change(function () {
        let selected_country = country_dropdown.val();
        let selected_city = city_dropdown.val();
        if (selected_country === "") {
            municipality_dropdown.find('option').not(':first').remove();
            city_dropdown.find('option').not(':first').remove();
            postcode_dropdown.find('option').not(':first').remove();
        } else {
            $.ajax({
                type: 'GET',
                data: {
                    enable_municipalities: '',
                    country: selected_country,
                    city: selected_city
                },
                url: '/property',
                beforeSend: function () {
                    municipality_dropdown.find('option').not(':first').remove();
                    city_dropdown.find('option').not(':first').remove();
                    postcode_dropdown.find('option').not(':first').remove();
                    disableInput();

                },
                success: function (resp) {
                    let municiHTML = ``;
                    let cityHTML = ``;
                    for (let i = 0; i < resp.data.length; i++) {
                        if (resp.data[i].municipalities == null) {
                            cityHTML += `<option value="${resp.data[i].cities}">${resp.data[i].cities}</option>`
                        } else {
                            municiHTML += `<option value="${resp.data[i].municipalities}">${resp.data[i].municipalities}</option>`
                        }
                    }
                    municipality_dropdown.append(municiHTML);
                    city_dropdown.append(cityHTML);
                },
                complete: function () {
                    enableInput();
                },
                error: function (xhr, status, error) {
                    // TODO: show toastr
                    console.error(error);
                    enableInput();
                },
            })
        }
    });
    //Municipalities->Cities
    municipality_dropdown.change(function () {
        let selected_municipality = municipality_dropdown.val();
        if (selected_municipality === "") {
            city_dropdown.find('option').not(':first').remove();
            postcode_dropdown.find('option').not(':first').remove();
        } else {
            $.ajax({
                type: 'GET',
                data: {
                    enable_cities: '',
                    municipality: selected_municipality,
                },
                url: '/property',
                beforeSend: function () {
                    city_dropdown.find('option').not(':first').remove();
                    postcode_dropdown.find('option').not(':first').remove();
                    disableInput();
                },
                success: function (resp) {
                    let newHTML = ``;
                    for (let i = 0; i < resp.data.length; i++) {
                        newHTML += `<option value = "${resp.data[i]}">${resp.data[i]}</option>`
                    }
                    city_dropdown.append(newHTML);
                },
                complete: function () {
                    enableInput();
                },
                error: function (xhr, status, error) {
                    // TODO: show toastr
                    console.error(error);
                    enableInput();
                },
            })
        }
    });
    //Cities->Postcodes
    city_dropdown.change(function () {
        let selected_city = city_dropdown.val();
        if (selected_city === "") {
            postcode_dropdown.find('option').not(':first').remove();
        } else {
            $.ajax({
                type: 'GET',
                data: {
                    enable_postcodes: '',
                    city: selected_city,
                },
                url: '/property',
                beforeSend: function () {
                    disableInput();
                },
                success: function (resp) {
                    let newHTML = ``;
                    for (let i = 0; i < resp.data.length; i++) {
                        newHTML += `<option value = "${resp.data[i]}">${resp.data[i]}</option>`
                    }
                    postcode_dropdown.append(newHTML);
                },
                complete: function () {
                    enableInput();
                },
                error: function (xhr, status, error) {
                    // TODO: show toastr
                    console.error(error);
                    enableInput();
                },
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
        $(filter).each(function (index, obj) {
            request_data[obj.name] = obj.value
        });
        $.ajax({
            url: '/property?' + $.param(request_data),
            type: 'GET',
            beforeSend: function () {
                hideElem(result_elem);
                property_overview.html('');
                result_elem.html('');
                showElem(loading_elem);
                disableInput();
            },
            success: function (resp) {
                let newHTML = resp.data.map(function (d) {
                    return propertyHTML(d)
                });
                if (newHTML === undefined || newHTML.length === 0) {
                    msg_area.append(showElem(result_elem.html('<h3>No results found!</h3>')));
                } else {
                    property_overview.append(newHTML.join(''));
                    search_box.val('');
                }
            },
            complete: function () {
                hideElem(loading_elem);
                enableInput();
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
                enableInput();
            },
        });
    }
    filter_button.on('click', function (e) {
        e.preventDefault();
        filter(e);
    });
    search_box.on('keypress', function (e) {
        if (e.which === 13) {
            filter(e);
        }
    });

    function purchaseStep1() {
        $('#purchase-paragraph').replaceWith('<h3 id="purchase-paragraph"></h3>');
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
