// $(document).ready(function() {
//     $('#forum_content').on("click", "#article", function(){
//         // 找到click的那個的 m_id 、 user_id
//         var m_id = $(this).find('.m_id').text();
//         var user_id = $(this).find('.user_id').text();
//         var f_id = $(this).find('.f_id').text();

//         // alert(m_id);
//         // alert(user_id);

//         $.ajax({
//             type: "GET",
//             url: "forum_article",
//             data: {
//                 m_id: m_id,
//                 user_id: user_id,
//                 f_id: f_id,
//             },
//             success: function(response) {
//                 // alert("123");
//                 window.location.href = "forum_article?m_id=" + m_id + "&user_id=" + user_id + "&f_id=" + f_id;
//             },
//             error: function(xhr, status, error) {
//                 console.error(error);
//             }
//         });

//     });
// });


$(document).ready(function() {
    $('#forum_content').on("click", "#article", function(){
        // 找到click的那個的 m_id 、 user_id
        var m_id = $(this).find('.m_id').text();
        var art_id = $(this).find('.art_id').text();

        // alert(m_id);

        $.ajax({
            type: "GET",
            url: "forum_article",
            data: {
                'm_id': m_id,
                'art_id': art_id,
            },
            success: function(response) {
                // alert("123");
                window.location.href = "forum_article?m_id=" + m_id + "&art_id=" + art_id;
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });

    });


    $("#openPopupButton").click(function() {
        var in_out = $('.user_in').text();
        if(in_out == 'in'){
            $("#popupForm").show();
            $("#overlay").show();        
        }
        else{
            alert("Log in to add a new article.")
        }
    });

    $("#closePopupButton").click(function(event) {
        event.preventDefault();
        $("#id_title").val("");
        $("#id_content").val("");
        $("#popupForm").hide();
        $("#overlay").hide();
    });

    $('.movie_title').on("click", function(){
        // 找到click的那個的 m_id 、 user_id
        var m_id = $('.film_id').text();
        // var art_id = $(this).find('.art_id').text();

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
    
});