$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    
    // get data from url
    var m_id = parseInt(urlParams.get('m_id'));
    var art_id = parseInt(urlParams.get('art_id'));

    // $('.forumID').text(f_id);
    // $('.movieID').text(m_id);
    var currentTime = new Date();

    // 格式化時間為 yyyy-mm-dd HH:MM:SS 格式
    var formattedTime = currentTime.getFullYear() + '-' +
                        ('0' + (currentTime.getMonth() + 1)).slice(-2) + '-' +
                        ('0' + currentTime.getDate()).slice(-2) + ' ' +
                        ('0' + currentTime.getHours()).slice(-2) + ':' +
                        ('0' + currentTime.getMinutes()).slice(-2) + ':' +
                        ('0' + currentTime.getSeconds()).slice(-2) + '.' +
                        ('00' + currentTime.getMilliseconds()).slice(-3);



    // 將格式化後的時間填入指定的元素中
    $('.current_time').text(formattedTime);


    $('#edit').on("click", function(){
        // alert('cli');

        // 修改時，影藏member 資訊
        $(".member").css("display", "none");

        // 內容修改
        var content = $(".content > h4").text().trim();
        $(".edit_content").css("display", "block");
        $(".content > span").css("display", "block");
        $(".content > h4").css("display", "none");
        // alert(content);

    
        $(".edit_content").val(content);

        // 修改button出現
        $(".edit_submit").css("display", "block");
        $(".edit_cancel").css("display", "block");


        // 修改標題
        var title = $(".title > h1").text().trim();
        $(".edit_title").css("display", "block");
        $(".title > span").css("display", "block");
        $(".title > h1").css("display", "none");
        // alert(content);


        $(".edit_title").val(title);
        // adjustTitleSize();
    });

    // 取消edit
    $('.edit_cancel').on("click", function(){
        $(".edit_cancel").css("display", "none");
        $(".edit_submit").css("display", "none");

        $(".edit_title").css("display", "none");
        $(".title > span").css("display", "none");
        $(".title > h1").css("display", "block");

        $(".edit_content").css("display", "none");
        $(".content > span").css("display", "none");
        $(".content > h4").css("display", "block");
    });

    // 送出修改
    $('.edit_submit').on("click", function(event){
        event.preventDefault();

        var title = $(".edit_title").val().trim();
        var content = $(".edit_content").val().trim();

        if (title.trim() === '') {
            Swal.fire({
                title: "Title can't be empty",
                confirmButtonText: "OK!",
                icon: "error"
            });
        } else if (content.trim() === '') {
            Swal.fire({
                title: "Content can't be empty",
                confirmButtonText: "OK!",
                icon: "error"
            });
        }
        else{
            $.ajax({
                url: 'forum_article',
                type: 'POST', 
                data: {
                    'title': title,
                    'content': content,
                    'mode' : 'forum_article_edit',
                    'm_id' : m_id,
                    'art_id' : art_id,
                },
                success: function(response){
                    Swal.fire({
                        icon: "success",
                        title: "The article has been successfully modified!",
                        confirmButtonText: "OK!",
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.reload(true);
                            console.log(response);
                        }
                    });
                },
                error: function(response){
                    alert("edit faild");
                    console.log(response);
                }
            });
        }
    });

    $('#delete').on("click", function(){
        Swal.fire({
            title: "Are you sure?",
            text: "You will delete the entire article!",
            icon: "warning",
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Yes, delete it.",
            showCancelButton: true,
            cancelButtonColor: "#d33",
          }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    title: "Deleted!",
                    icon: "success",
                    text: "Your article has been deleted.",
                    confirmButtonText: "OK!",
                }).then((result) => {
                    if (result.isConfirmed) {
                        $.ajax({
                            url: 'forum_article',
                            type: 'POST', 
                            data: {
                                'mode' : 'forum_article_delete',
                                'm_id' : m_id,
                                'art_id' : art_id,
                            },
                            success: function(response){
                                console.log(response);
                                window.location.href = "forum?m_id=" + m_id;
                            },
                            error: function(response){
                                alert("delete faild");
                                console.log(response);
                            }
                        });
                    }
                });        
            }
          });
    });
    
    $('.cancel_button').on("click", function(event){
        $("#post-text").val("");
    });

    $('.submit_button').on("click", function(event){
        var content = $('#id_conent').val();
        console.log(content);
        if (content.trim() === ''){
            event.preventDefault();
            Swal.fire({
                title: "Message can't be empty",
                confirmButtonText: "OK!",
                icon: "error"
            });
        }
    });
    $('.mess_cancel_button').on("click", function(event){
        $("#id_conent").val("");
    });

    $('.mess_edit').on("click", function(event){
        event.preventDefault();
        var postMessage = $(this).closest('.one_mess').find('.post_message');
        var content = postMessage.find('.orignal_contnet').text().trim();
        // alert(content);
        // var id = $(".com_id").text().trim();
        // alert(content)
        postMessage.find(".orignal_contnet").css("display", "none");
        postMessage.find(".edit_mess_content").css("display", "block");
        postMessage.find(".edit_mess_content").val(content);

        postMessage.find(".mess_button").css("display", "flex");

    });

    $('.mess_cancel_button').on("click", function(event){
        var postMessage = $(this).closest('.one_mess').find('.post_message');

        postMessage.find(".orignal_contnet").css("display", "block");
        postMessage.find(".edit_mess_content").css("display", "none");       

        postMessage.find(".mess_button").css("display", "none");       

    });

    $('.mess_submit_button').on("click", function(event){
        var content = $(this).closest('.post_message').find('.edit_mess_content').val();
        var id = $(this).closest('.post_message').find('.com_id').text().trim();

        if (content.trim() === ''){
            Swal.fire({
                title: "Message can't be empty",
                confirmButtonText: "OK!",
                icon: "error"
            });
        }
        else{
            $.ajax({
                url: 'forum_article',
                type: 'POST', 
                data: {
                    'content': content,
                    'mode' : 'forum_message_edit',
                    'm_id' : m_id,
                    'art_id' : art_id,
                    'acom_id' : id,
                },
                success: function(response){
                    Swal.fire({
                        icon: "success",
                        title: "Your message has been saved",
                        confirmButtonText: "OK!",
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.reload();
                        }
                    });
                },
                error: function(response){
                    alert("edit faild");
                    console.log(response);
                }
            });
        }

    });

    // mess_delete
    $('.mess_delete').on("click", function(event){
        var postMessage = $(this).closest('.one_mess').find('.post_message');
        
        var ac_id = postMessage.find(".com_id").text().trim();

        Swal.fire({
            title: "Are you sure?",
            text: "You will delete the comment!",
            icon: "warning",
            confirmButtonColor: "#3085d6",
            confirmButtonText: "Yes, delete it.",
            showCancelButton: true,
            cancelButtonColor: "#d33",
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: 'forum_article',
                    type: 'POST', 
                    data: {
                        'mode' : 'forum_message_delete',
                        'ac_id' : ac_id,
                    },
                    success: function(response){
                        Swal.fire({
                            icon: "success",
                            title: "Your comment has been deleted",
                            confirmButtonText: "OK!",
                        }).then((result) => {
                            if (result.isConfirmed) {
                                location.reload();
                                console.log(response);
                            }
                        });
                    },
                    error: function(response){
                        alert("delete faild");
                        console.log(response);
                    }
                });      
            }
          });
    });

    // 選擇所有的img元素
    var images = document.querySelectorAll('img');

    // 對每個img元素添加點擊事件監聽器
    images.forEach(function(image) {
        image.addEventListener('click', function() {
            // 獲取img元素對應的成員ID
            var memberId = this.getAttribute('data-userid');
            // console.log("UID:", memberId);

            // 獲取CSRF令牌
            var csrftoken = getCookie('csrftoken');

            // 發送POST請求，包含CSRF令牌
            $.ajax({
                url: '/chat/addfriend',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'mode': 'addFriends',
                    'be_uid': memberId,
                },
                success: function(response) {
                    console.log(response);
                    // alert('success');
                    window.location.href = '/chat/'; // 在成功回應後進行跳轉
                },
                error: function(response) {
                    console.log(response);
                }
            });
            // 這裡可以進一步處理獲取的ID
        });
    });

    $('.movie_name').on("click", function(){
        // 找到click的那個的 m_id 、 user_id
        var m_id = $('.film_id').text();
        // alert(m_id);
        window.location.href = "movie?m_id=" + m_id;

    });
});