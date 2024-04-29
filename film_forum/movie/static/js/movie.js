$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    
    // get data from url
    var m_id = parseInt(urlParams.get('m_id'));
    // alert(m_id);

    // $('.more_forum').on("click", function(){    
    //     $.ajax({
    //         type: "POST",
    //         url: "movie",
    //         data: {
    //             m_id: m_id,
    //         },
    //         success: function(response) {
    //             alert("123");
    //             // window.location.href = "forum?m_id=" + m_id;
    //         },
    //         error: function(xhr, status, error) {
    //             console.error(error);
    //         }
    //     });  
    // });

    $('.more_forum').on("click", function(){
        // 找到click的那個的 m_id 、 user_id
        // var m_id = $('.movie_id').text();
     

        $.ajax({
            type: "GET",
            url: "forum",
            data: {
                m_id: m_id,
            },
            success: function(response) {
                // alert("123");
                window.location.href = "forum?m_id=" + m_id;
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });

    });
});


