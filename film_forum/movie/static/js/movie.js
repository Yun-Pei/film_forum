$(document).ready(function() {
    $('.more_forum').on("click", function(){
        // 找到click的那個的 m_id 、 user_id
        var m_id = $('.movie_id').text();
        // var user_id = $(this).find('.user_id').text();
        // var f_id = $(this).find('.f_id').text();

        // alert(m_id);
        // alert(user_id);

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


