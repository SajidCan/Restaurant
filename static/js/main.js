// $('.slicky').slick({
//    autoplay:false,
//    slidesToShow: 2,
//    speed: 500,
//    arrows: true,
//    prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
//    nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
// });
$('.slicky').slick({
  autoplay:false,
  slidesToShow: 3,
  speed: 500,
  arrows: true,
  responsive: [
 {
   breakpoint: 1024,
   settings: {
     slidesToShow: 3,
     slidesToScroll: 3,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"

   }
 },
 {
   breakpoint: 769,
   settings: {
     slidesToShow: 2,
     slidesToScroll: 2,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
   }
 },
 {
   breakpoint: 590,
   settings: {
     slidesToShow: 1,
     slidesToScroll: 1,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
   }
 }
],
prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
});

$('.review_slicky').slick({
  autoplay:false,
  slidesToShow: 2,
  speed: 500,
  arrows: true,
  responsive: [
 {
   breakpoint: 1024,
   settings: {
     slidesToShow: 2,
     slidesToScroll: 2,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"

   }
 },
 {
   breakpoint: 769,
   settings: {
     slidesToShow: 1,
     slidesToScroll: 1,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
   }
 },
 {
   breakpoint: 480,
   settings: {
     slidesToShow: 1,
     slidesToScroll: 1,
     prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
     nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
   }
 }
],
prevArrow:"<button type='button' class='slick-prev pull-left'><i class='fa fa-angle-left' aria-hidden='true'></i></button>",
nextArrow:"<button type='button' class='slick-next pull-right'><i class='fa fa-angle-right' aria-hidden='true'></i></button>"
});


var close = document.getElementsByClassName("closebtn");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}
