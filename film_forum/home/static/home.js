$(document).ready(function() {
    $('.swiper-slide').on("click", function(){
        var m_id = $(this).find('.m_id').text(); 
        // alert(m_id);

        window.location.href = "movie?m_id=" + m_id;
    });
    
});