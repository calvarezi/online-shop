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
      speed: 3000, // Ajustar la velocidad de transición
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
  $(".novedad-image").css("display", "flex"); // Ajusta el valor de margen según tus necesidades4
  $(".novedad-image").css("gap", "5px"); // Ajusta el valor de margen según tus necesidades4
});

$(document).ready(function () {
  $(".carousel__item").slick({
    infinite: true,
    slidesToShow: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    arrows: false,
    adaptiveHeight: true,
    centerPadding: "70 px ",
    lazyLoad: "ondemand",
    speed: 3000,
  });
});
