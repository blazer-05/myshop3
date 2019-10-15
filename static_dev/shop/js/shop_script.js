
// Скрипт который выводит в модальном окне товар на главной странице если нажать на значок лупы.
$('#productModal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget);
  let url = button.data('url');
  let container = $(this).find('.modal-product');
  container.html('');
  $.ajax({
    url: url,
  }).done(function(data){
    container.html(data);
  });
});


// Для owl карусели которая в шаблоне index-carousel.html и выводится на главной
// в блоке категорий
function set_owl_on_active_product_carosel(elements) {
    elements.owlCarousel({
      autoPlay: false,
      slideSpeed: 2000,
      pagination: false,
      navigation: true,
      items: 4,
      navigationText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
      itemsDesktop: [1169, 3],
      itemsTablet: [991, 2],
      itemsTabletSmall: [767, 2],
      itemsMobile: [479, 1],
    });
  }


// аякс запрос для вывода на главной ссылок списка брендов, по клику отображается товар данного бренда
// второй клик по текущему бренду отображает все товары.
$(function ($) {
  $('.jq_sort_brand').click(function (event) {
    event.preventDefault();
    let url = '';
    let a = $(this);
    let li = a.parent();
    if(li.hasClass('active')) {
      url = li.parent().data('default-url');
    } else {
      li.siblings().removeClass('active');
      url = a.data('url')
    }
    li.toggleClass('active');

    fetch(url, {
      method: 'GET',
    }).then(function (res) {
      res.text().then(function (text) {
        a.closest('.product-area')
          .find('.active-product-carosel')
          .unbind()
          .removeData()
          .html(text)
          .owlCarousel({
            autoPlay: false,
            slideSpeed: 2000,
            pagination: false,
            navigation: true,
            items: 4,
            navigationText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            itemsDesktop: [1169, 3],
            itemsTablet: [991, 2],
            itemsTabletSmall: [767, 2],
            itemsMobile: [479, 1],
          });
      })
    });
  });
});


/*---------------------
 price slider
--------------------- */
  $(function() {
    let min_price_el = $("#id_min_price");
    let max_price_el = $("#id_max_price");
    let sliderRange = $( "#slider-range" );
    let minValue = sliderRange.data('min');
    let maxValue = sliderRange.data('max')

    let updateRangeFields = function (minValue, maxValue) {
      min_price_el.val(minValue);
      max_price_el.val(maxValue);
    };

    let updateSlider = function (min_value, max_value) {
      sliderRange.slider("option", "values", [ min_value, max_value ]);
    };

    let bindChangeEvents = function(el) {
      el
        .change(function () {
          updateSlider(min_price_el.val(), max_price_el.val());
        })
        .keyup(function () {
          updateSlider(min_price_el.val(), max_price_el.val());
        });
    };

    sliderRange.slider({
     range: true,
     min: minValue,
     max: maxValue,
     values: [ min_price_el.val(), max_price_el.val() ],
     slide: function( event, ui ) {
       updateRangeFields(ui.values[0], ui.values[1])
     }
    });
    updateRangeFields(min_price_el.val(), max_price_el.val());
    bindChangeEvents(min_price_el);
    bindChangeEvents(max_price_el);
  });


//Слайдер на главной странице
$(document).ready(function(ev){
    var items = $(".nav li").length;
    var leftRight=0;
    if(items>5){
        leftRight=(items-5)*50*-1;
    }
    $('#custom_carousel').on('slide.bs.carousel', function (evt) {


      $('#custom_carousel .controls li.active').removeClass('active');
      $('#custom_carousel .controls li:eq('+$(evt.relatedTarget).index()+')').addClass('active');
    })
    $('.nav').draggable({
        axis: "x",
         stop: function() {
            var ml = parseInt($(this).css('left'));
            if(ml>0)
            $(this).animate({left:"0px"});
                if(ml<leftRight)
                    $(this).animate({left:leftRight+"px"});

        }

    });
});

