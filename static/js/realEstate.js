$(document).ready(function () {
    function search(e) {
        let searchText = $('#search-box').val();
        $.ajax({
            url: '/property?search_filter=' + searchText,
            type: 'GET',
            success: function (resp) {
                let newHTML = resp.data.map(d => {
                    console.log(d) // temp
                    return `<a href="/property/${d.id}" class="link-to-property">
                                <div class="card property">
                                    <img class="property-img" src="${d.firstImage}"/>
                                    <div class="card-body">    
                                        <h5 class="card-title">${d.name}</h5>
                                        <h6 class="card-subtitle mb-2">${d.price} $</h6>
                                        <p class="card-text">Size ${d.squareMeters}m<sup>2</sup>, ${d.nrBedrooms} bedrooms, ${d.nrBathrooms} bathrooms</p>
                                    </div>
                                </div>
                            </a>`
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
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        let search_filter = document.getElementById('search-box')
        let country_field = document.getElementById('country_dropd');
        let price_from_field = document.getElementById('price_from_dropd');
        let price_to_field = document.getElementById('price_to_dropd');
        let size_from_field = document.getElementById('size_from_dropd');
        let size_to_field = document.getElementById('size_to_dropd');
        let rooms_from_field = document.getElementById('rooms_from_dropd');
        let rooms_to_field = document.getElementById('rooms_to_dropd');
        let type_field = document.getElementById('type_dropd');
        let request_data = {
            search_filter: search_filter.value,
            country_field: country_field.value,
            price_from_field: price_from_field.value,
            price_to_field: price_to_field.value,
            size_from_field: size_from_field.value,
            size_to_field: size_to_field.value,
            rooms_from_field: rooms_from_field.value,
            rooms_to_field: rooms_to_field.value,
            type_field: type_field.value,
        };
        $.ajax({
            url: '/property?' + $.param(request_data),
            type: 'GET',
            success: function (resp) {
                let newHTML = resp.data.map(function(d) {
                    return `<a href="/property/${d.id}" class="link-to-property">
                                <div class="card property">
                                    <img class="property-img" src="${d.firstImage}"/>
                                    <div class="card-body">    
                                        <h5 class="card-title">${d.name}</h5>
                                        <h6 class="card-subtitle mb-2">${d.price} $</h6>
                                        <p class="card-text">Size ${d.squareMeters}m<sup>2</sup>, ${d.nrBedrooms} bedrooms, ${d.nrBathrooms} bathrooms</p>
                                    </div>
                                </div>
                            </a>`
                });
                $('.property-overview').html(newHTML.join(''));
                $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
            },
        });
    });
});