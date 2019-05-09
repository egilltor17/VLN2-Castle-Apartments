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
   // $('#filter_props').on('click', function(e) {
   //
   // });
});