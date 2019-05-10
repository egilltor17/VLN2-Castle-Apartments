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
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        let filters = $('#filter-form').serialize();
        // let request_data = {
        //     search_field: search_field.value,
        //     country_field: country_field.value,
        //     price_from_field: price_from_field.value,
        //     price_to_field: price_to_field.value,
        //     size_from_field: size_from_field.value,
        //     size_to_field: size_to_field.value,
        //     rooms_from_field: rooms_from_field.value,
        //     rooms_to_field: rooms_to_field.value,
        //     type_field: type_field.value
        // };

        $.ajax({
            url: '/property?' + filters,
            type: 'GET',
            success: function (resp) {
                console.log(resp);
                // let newHTML = resp.data.map(function(d) {
                //     return `<div class="card">
                //                 <a href="/property/${d.id}">
                //                     <img class="property-img" src="${d.firstImage}"/>
                //                     <h4>${d.name}</h4>
                //                     <p>${d.price} $</p>
                //                     <p>${d.description}</p>
                //                     <p>${d.address.country}</p>
                //                 </a>
                //             </div>`
                // });
                // $('.property-overview').html(newHTML.join(''));
                // $('#search-box').val('');
            },
            error: function (xhr, status, error) {
                // TODO: show toastr
                console.error(error);
            },
        });
    });
});