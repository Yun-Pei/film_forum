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
                'm_id' : m_id,
                'art_id' : art_id,
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
        // alert(m_id)
        // delete
        if(answer){
            $.ajax({
                url: 'forum_article',
                type: 'POST', 
                data: {
                    'mode' : 'forum_article_delete',
                    'm_id' : m_id,
                    'art_id' : art_id,
                },
                success: function(response){
                    // alert("POST arleady")
                    alert("The article has been successfully deleted! The page will now return to the discussion board.")
                    console.log(response);
                    // window.location.href = 'forum';
                },
                error: function(response){
                    alert("delete faild");
                    console.log(response);
                }
            });            
        }
    });
    
    $('.cancel_button').on("click", function(event){
        $("#post-text").val("");
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

        // alert(content);
        // alert(id);

        if (content == ''){
            alert("Can't empty");
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
                    // alert("POST arleady")
                    alert("The message has been successfully modified!");
                    console.log(response);
                    location.reload(true);
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
        let answer = confirm('Delete the comment?');
        // alert(ac_id);
        // delete
        if(answer){
            $.ajax({
                url: 'forum_article',
                type: 'POST', 
                data: {
                    'mode' : 'forum_message_delete',
                    'ac_id' : ac_id,
                },
                success: function(response){
                    // alert("POST arleady")
                    alert("Successfully deleted!")
                    console.log(response);
                    location.reload(true);
                },
                error: function(response){
                    alert("delete faild");
                    console.log(response);
                }
            });                 
        }

    });
});