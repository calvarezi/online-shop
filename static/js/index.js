$(document).ready(function () {
  function initializeSlick() {
    $(".carousel__group").slick({
      slidesToShow: 2, // Cambiar a 2 para mostrar dos imágenes por grupo
      slidesToScroll: 2,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 3000,
      prevArrow: false,
      nextArrow: false,
      rows: 2,
      speed: 1000, // Ajustar la velocidad de transición
    });
  }

  initializeSlick(); // Inicializar Slick al cargar la página

  $(".carousel__group").on(
    "beforeChange",
    function (event, slick, currentSlide, nextSlide) {
      if (nextSlide === 0) {
        $(".carousel__group").slick("slickGoTo", slick.slideCount); // Cambiar al último grupo de imágenes
      }
    }
  );
});

$(document).ready(function(){
  $('.carousel__item').slick({
      infinite: true,
      slidesToShow: 1,
      autoplay: true,
      autoplaySpeed: 1000,
      arrows: false,
  });
});