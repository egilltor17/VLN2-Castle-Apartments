$(document).ready(function () {
    function search(e) {
        let searchText = $('#search-box').val();
        $.ajax({
            url: '/property?search_filter=' + searchText,
            type: 'GET',
            success: function (resp) {
                let newHTML = resp.data.map(d => {
                    console.log(d)
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
                    /*
                    <a href="/property/{{ property.id }}" class="link-to-property">
                        <div class="card property" >
                            <img class="property-img" src="{{ property.propertyimage_set.first.image }}"/>

                                <h5 class="card-title">{{ property.name }}</h5>
                                <h6 class="card-subtitle mb-2">{{ property.price }} $</h6>
                                <p class="card-text">Size {{ property.squareMeters }}m<sup>2</sup>, {{ property.nrBedrooms }} bedrooms, {{ property.nrBathrooms }} bathrooms</p>
                            </div>
                        </div>
                    </a>
                    */

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
});