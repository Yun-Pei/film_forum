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

    $('#forum_content').on("click", "#article", function(){
        // 找到click的那個的 m_id 、 user_id
        var m_id = $('.movie_id').text();
        var art_id = $(this).find('#art_id').text();
        // alert(m_id)

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

    $('.movie_comment_delete').on("click", function(){
        // alert("123");
        let answer = confirm('Are you sure you want to delete the review?');
        // var Comment_id = $(this).find('#Comment_id').text();
        var Comment_id = $(this).find('.Comment_id').text().trim();

        // alert(Comment_id)
        // delete
        if(answer){
            $.ajax({
                url: 'movie',
                type: 'GET', 
                data: {
                    'mode' : 'movie_comment_delete',
                    'm_id' : m_id,
                    'Comment_id' : Comment_id,
                },
                success: function(response){
                    // alert("POST arleady")
                    alert("The comment has been successfully deleted!")
                    console.log(response);
                    location.reload();
                },
                error: function(response){
                    alert("delete faild");
                    console.log(response);
                }
            });
        }
    });
});


