$(document).ready(function () {
    function search(e) {
        let searchText = $('#search-box').val();
        $.ajax({
            url: '/property?search_filter=' + searchText,
            type: 'GET',
            success: function (resp) {
                let newHTML = resp.data.map(d => {
                    return `<div class="well property">
                                <a href="/property/${d.id}">
                                    <img class="property-img" src="${d.firstImage}"/>
                                    <h4>${d.name}</h4>
                                    <p>${d.price} $</p>
                                    <p>${d.description}</p>
                                    <p>${d.address.country}</p>
                                </a>
                            </div>`
                });
                $('.property-overview').html(newHTML.join(''));
                $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
            },
        });
    };
    $('#search-btn').on('click', function (e) {
        e.preventDefault();
        search(e);
    });
    $('#search-box').on('keypress', function (e) {
        if(e.which == 13) {
            search(e);
        }
    });
    $('#filter_props').on('click', function(e) {
        // it's meant to return a new page below with the properties it found
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        let search_field = document.getElementById('search-box')
        let country_field = document.getElementById('country_dropd');
        let price_from_field = document.getElementById('price_from_dropd');
        let price_to_field = document.getElementById('price_to_dropd');
        let size_from_field = document.getElementById('size_from_dropd');
        let size_to_field = document.getElementById('size_to_dropd');
        let rooms_from_field = document.getElementById('rooms_from_dropd');
        let rooms_to_field = document.getElementById('rooms_to_dropd');
        let type_field = document.getElementById('type_dropd');
        let request_data = {
            country_field: country_field.value,
            price_from_field: price_from_field.value,
            price_to_field: price_to_field.value,
            size_from_field: size_from_field.value,
            size_to_field: size_to_field.value,
            rooms_from_field: rooms_from_field.value,
            rooms_to_field: rooms_to_field.value,
            type_field: type_field.value,
            search_field: search_field.value
        };
        //
        $.ajax({
            url: '/property?' + $.param(request_data),
            type: 'GET',
            success: function (resp) {
                let newHTML = resp.data.map(function(d) {
                    return `<div class="well property">
                                <a href="/property/${d.id}">
                                    <img class="property-img" src="${d.firstImage}"/>
                                    <h4>${d.name}</h4>
                                    <p>${d.price} $</p>
                                    <p>${d.description}</p>
                                    <p>${d.address.country}</p>
                                </a>
                            </div>`
                });
                $('.property-overview').html(newHTML.join(''));
                // $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
            },
        });
    });
});