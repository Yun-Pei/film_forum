var swiper = new Swiper(".swiper", {
    effect:"coverflow", 
    grabCursor: true, 
    centeredSlides: true,
    initialSlide: 2,
    speed: 600,
    preventClicks: true,
    slidesPerView: "auto",
    coverflowEffect: {
        rotate: 0,
        stretch: 0,
        depth: 350,
        modifier: 1,
        slideShadows: true,
        scale:  .85,
    },
    on:{
        click(event){
            swiper.slideTo(this.clickedIndex);
        },
    },
    paginaiton: {
        el:".swiper-pagination",
    },
});

// var swiper = new Swiper(".myswiper", {
//     effect:"coverflow", 
//     grabCursor: true, 
//     centeredSlides: true,
//     initialSlide: 2,
//     speed: 600,
//     preventClicks: true,
//     slidesPerView: "auto",
//     coverflowEffect: {
//         rotate: 0,
//         stretch: 80,
//         depth: 350,
//         modifier: 1,
//         slideShadows: true, 
//     },
//     on:{
//         click(event){
//             swiper.slideTo(this.clickedIndex);
//         },
//     },
//     paginaiton: {
//         el:".swiper-pagination",
//     },
// });