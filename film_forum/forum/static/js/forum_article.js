$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    
    // get data from url
    var m_id = parseInt(urlParams.get('m_id'));
    var user_id = parseInt(urlParams.get('user_id'));
    var f_id = parseInt(urlParams.get('f_id'));

    $('.forumID').text(f_id);
    $('.movieID').text(m_id);
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

    $.ajax ({
        type: "GET",
        url: "forum_article",
        data: {
            'm_id': m_id,
            'user_id': user_id,
            'f_id': f_id,
            'mode': "which_article",
        },
        success: function(response){
            console.log('OK');
        },
        error: function(response){
            alert("輸入失敗");
            console.log(response);
        }
    });


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

        // 调整 textarea 的大小
        function adjustTextareaSize() {
            // 設置為滾動大小的高度
            $(".edit_content").css("width", "100%");
            $(".edit_content").css("height", $(".edit_content").prop("scrollHeight") + "px");

        }

        // 當textarea 有input資料後 實行調整大小
        $(".edit_content").on("input", adjustTextareaSize);

    
        $(".edit_content").val(content);
        adjustTextareaSize();


        // 修改button出現
        $(".edit_submit").css("display", "block");
        $(".edit_cancel").css("display", "block");


        // 修改標題
        var title = $(".title > h2").text().trim();
        $(".edit_title").css("display", "block");
        $(".title > span").css("display", "block");
        $(".title > h2").css("display", "none");
        // alert(content);

        // 调整 textarea 的大小
        function adjustTitleSize() {
            // 設置為滾動大小的高度
            $(".edit_title").css("width", "100%");
            $(".edit_title").css("height", $(".edit_title").prop("scrollHeight") + "px");

        }

        // 當textarea 有input資料後 實行調整大小
        $(".edit_title").on("input", adjustTitleSize);

    
        $(".edit_title").val(title);
        adjustTitleSize();
    });

    // 取消edit
    $('.edit_cancel').on("click", function(){
        $(".edit_cancel").css("display", "none");
        $(".edit_submit").css("display", "none");

        $(".edit_title").css("display", "none");
        $(".title > span").css("display", "none");
        $(".title > h2").css("display", "block");

        $(".edit_content").css("display", "none");
        $(".content > span").css("display", "none");
        $(".content > h4").css("display", "block");
    });

    // 送出修改
    $('.edit_submit').on("click", function(event){
        event.preventDefault();

        var title = $(".edit_title").val().trim();
        var content = $(".edit_content").val().trim();

        // alert(content);
        $.ajax({
            url: 'forum_article',
            type: 'POST', 
            data: {
                'title': title,
                'content': content,
                'mode' : 'forum_article_edit',
                'm_id': m_id,
                'user_id': user_id,
                'f_id': f_id,
            },
            success: function(response){
                // alert("POST arleady")
                alert("The article has been successfully modified!")
                console.log(response);
                location.reload(true);
            },
            error: function(response){
                alert("edit faild");
                console.log(response);
            }
        });
    });

    $('#delete').on("click", function(){
        let answer = confirm('Are you sure you want to delete the entire article?');

        // delete
        if(answer){
            $.ajax({
                url: 'forum_article',
                type: 'POST', 
                data: {
                    'mode' : 'forum_article_delete',
                    'm_id': m_id,
                    'user_id': user_id,
                    'f_id': f_id,
                },
                success: function(response){
                    // alert("POST arleady")
                    alert("The article has been successfully deleted! The page will now return to the discussion board.")
                    console.log(response);
                    window.location.href = 'forum';
                },
                error: function(response){
                    alert("delete faild");
                    console.log(response);
                }
            });            
        }
    });

    // $('.submit_button').on("click", function(event){
    //     event.preventDefault();

    //     $.ajax({
    //         url: 'forum_article',
    //         type: 'POST', 
    //         data: {
    //             'm_id': m_id,
    //             'user_id': user_id,
    //             'f_id': f_id,
    //         },
    //         success: function(response){
    //             alert("POST arleady")
    //             console.log(response);
    //             $('#Message_form').submit();
    //         },
    //         error: function(response){
    //             alert("faild");
    //             console.log(response);
    //         }
    //     });
    // });
    

});