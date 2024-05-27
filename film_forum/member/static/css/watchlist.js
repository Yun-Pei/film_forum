$(document).ready(function() {
  // alert('success');
  $('.turntomovie').on("click", function(){
      var m_id = $(this).find('.m_id').text(); 
      // alert(m_id);
      
      $.ajax({
          type: "GET",
          url: "movie",
          data: {
              'm_id': m_id,
          },
          success: function(response) {
              // alert("123");
              window.location.href = "movie?m_id=" + m_id;
          },
          error: function(xhr, status, error) {
              console.error(error);
          }
      });
  });
    $('.movieFav').on("click", function(){
    var m_id = $(this).find('.m_id').text(); 
    // alert(m_id);
    
        $.ajax({
            type: "POST",
            url: "watchlist",
            data: {
                'm_id': m_id,
                'mode': 'unfollow'
            },
            success: function(response) {
                // alert("123");
                console.log(response);
                location.reload(true);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
  
});