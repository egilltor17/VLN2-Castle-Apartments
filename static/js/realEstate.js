$(document).ready(function () {
    let loading = '<div id="loading"><p><img src="/media/icons/ajax-loader.gif" alt="Loading..."></p></div>'
    let result_msg = '<div id="result-msg"></div>'
    if (window.location.pathname === '/property/')
    {
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
});