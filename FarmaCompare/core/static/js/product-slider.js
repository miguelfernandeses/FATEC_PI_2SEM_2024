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


let count = 1;
document.getElementById("radio1").checked = true;

setInterval( function(){
nextImage();
},2000)

function nextImage(){
    count++;
    if(count>4){
        count = 1;
    }

    document.getElementById("radio"+count).checked = true;
}