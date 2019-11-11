
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
 price slider - относится к фильтрам товаров.
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


// Запись в куку id товара
$('.compare, .toch-compare').click(function(e) {
  e.preventDefault();
  let pk = '' + $(this).data('product');
  let compare = Cookies.get('compare');
  if (compare === undefined)
    compare = '';
  let compare_list = compare === '' ? [] : compare.split(':');
  let index = compare_list.indexOf(pk);
  if (index > -1) {
      compare_list.splice(index, 1);
      $(this).removeClass('in-compare')
    } else {
      compare_list.push(pk);
      $(this).addClass('in-compare')
    }
  Cookies.set('compare', compare_list.join(':'));
  compareBadgeUpdate()
});

//Подсветка кнопки compare добавленных для сравнения товаров
$('.compare, .toch-compare').each(function(){
  let pk = '' + $(this).data('product');
  let compare = Cookies.get('compare');
  if (compare === undefined)
    compare = '';
  let compare_list = compare === '' ? [] : compare.split(':');
  if(compare_list.indexOf(pk) > -1)
    $(this).addClass('in-compare')
});


// Удаление товаров из compare (шаблон compare.html)
$('#compare_delete_product').on('click', function () {
  var r = confirm("Удалить все товары из сравнения?");
  if (r) {
    Cookies.set('compare', '');
    window.location.reload()
  }
});


// Количество добавленого товара в шаблоне base.html
function compareBadgeUpdate() {
  let compare = Cookies.get('compare');
  if (compare === undefined)
    compare = '';
  let count = compare === '' ? 0 : compare.split(':').length;
  $('.compare-badge').text(count);
}
compareBadgeUpdate();


//На кнопке compare срабатывает по клику подсказка "Добавлено"
// $(function () {
//   $('#prod_compare').popover({
//     trigger: 'focus',
//     fallbackPlacement: [],
//   })
// });






