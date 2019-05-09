$(document).ready(function () {
   $('#search-btn').on('click', function (e) {
      e.preventDefault();
      var searchText = $('#search-box').val();
      $.ajax( {
          url: '/property?search_filter=' + searchText,
          type: 'GET',
          success: function (resp) {
              var newHTML = resp.data.map(d => {
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
              $('.property').html(newHTML.join(''));
              $('#search-box').val('');
          },
          error: function (xhr,status, error) {
              // TODO: show toastr
              console.error(error);
          },
      });
   });
   $('#filter_props').on('click', function(e) {
        let country = $('#country_dropd').val();
        let price_from = $('#price_from_dropd').val();
        let price_to = $('#price_to_dropd').val();
        let size_from = $('#size_from_dropd').val();
        let size_to = $('#size_to_dropd').val();
        let rooms_from = $('#rooms_from_dropd').val();
        let rooms_to = $('#rooms_to_dropd').val();
        let type = $('#type_dropd').val();
        $.ajax()

   });
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
});