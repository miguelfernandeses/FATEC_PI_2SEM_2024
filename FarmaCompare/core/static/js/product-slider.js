$(document).ready(function(){
    $('.product-container').slick({
        infinite: true, 
        slidesToShow: 5, 
        slidesToScroll: 2, 
        autoplay: true, 
        autoplaySpeed: 4000, 
        responsive: [
            {
                breakpoint: 768, 
                settings: {
                    slidesToShow: 1, 
                }
            }
        ]
    });
});
