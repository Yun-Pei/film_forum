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
    
    // const swalWithBootstrapButtons = Swal.mixin({
    //     customClass: {
    //         confirmButton: "btn btn-success",
    //         cancelButton: "btn btn-danger"
    //     },
    //     buttonsStyling: false
    // });
    
    $('.movie_comment_delete').on("click", function(){
        // alert("123");
        // let answer = confirm('Are you sure you want to delete the review?');
        // var Comment_id = $(this).find('#Comment_id').text();
        var Comment_id = $(this).find('.Comment_id').text().trim();
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, delete it!"
        }).then((result) => {
            if(result.isConfirmed) {
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
                        Swal.fire({
                            title: "Deleted!",
                            text: "Your review has been deleted.",
                            icon: "success"
                        }).then((result) => {
                            // 弹窗关闭后刷新页面，无论是通过点击OK还是其他方式关闭弹窗
                            location.reload();
                        });
                        console.log(response);
                    },
                    error: function(response){
                        Swal.fire({
                            icon: 'error',
                            title: 'Oops...',
                            text: 'Something went wrong!',
                        });
                        console.log(response);
                    }
                });
            }else if (
                /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
            ) {
                Swal.fire({
                    title: "Cancelled",
                    text: "Your review is safe :)",
                    icon: "error"
                });
            }
        // alert(Comment_id)
        // delete
        
        });
    });

    $('.movie_comment_edit').on('click', function(event){
        event.preventDefault();
        // var content = $(".userReivew_cont > p").text().trim();
        var content = $(this).closest('.userReview_score').nextAll('.userReview_cont').first().find('.original_content').text().trim();
        // console.log('123', content);

        
        // $('.original_content').css('display', 'none');
        // $('.edit_review_content').css('display', 'block');
        // $('.edit_review_content').val(content);
        // $('.review_buttons').css('display', 'flex');
        var commentId = $(this).data('id');
        // console.log(commentId);
        $('.original_content[data-id="' + commentId + '"]').css('display', 'none');
        $('textarea.edit_review_content[data-id="' + commentId + '"]').css('display', 'block');
        $('textarea.edit_review_content[data-id="' + commentId + '"]').val(content);
        $('.review_buttons').css('display', 'flex');
    });

    $('.review_cancel_edit').on("click", function(event){
        $(".original_content").css("display", "block");
        $(".edit_review_content").css("display", "none");       
        $(".review_buttons").css("display", "none");       
    });

    $('.review_submit_edit').on('click', function() {
        // var content = ("textarea.edit_review_content").val();
        // var content = $(this).closest('.review_buttons').nextAll('.userReview_cont').first().find('.edit_review_content').val();
        var content = $(this).closest('.userReviewBox').find('.edit_review_content').val();

        var Comment_id = $(this).find('.Comment_id').text().trim();
        // alert(content);
        if (content == ''){
            alert("Can't be empty");
        }else {
            $.ajax({
                url: 'movie',
                type: 'GET', 
                data: {
                    'content': content,
                    'mode' : 'movie_comment_edit',
                    'm_id' : m_id,
                    'Comment_id' : Comment_id,
                },
                success: function(response){
                    // alert("POST arleady")
                    // alert("The review has been successfully edited!");
                    console.log(response);
                    location.reload(true);
                },
                error: function(response){
                    // alert("edit faild");
                    console.log(response);
                }
            });
        }
    });

    $('.FavoriteBtn').on('click', function(event) {
        // console.log('1111111');
        $.ajax({
            url: 'movie',
            type: 'POST',
            data: {
                'mode': 'unfollow',
                'm_id' : m_id,
            },
            success: function(response) {
                // alert('2111111')
                console.log(response)
            },
            error: function(reaponse) {
                // alert('1111211')
                console.log(reaponse)
            }
        });
        // alert(m_id);
    });

    $('.followBox').on('click', function(event) {
        console.log('followBox');
        $.ajax({
            url: 'movie',
            type: 'POST',
            data: {
                'mode': 'addfollow',
                'm_id': m_id,
            },
            success: function(response) {
                console.log(response)
            },
            error: function(reaponse) {
                console.log(reaponse)
            }
        });
    });
})
