
// Скрипт подтверждение удаления товара
$('#delete_my_orders').click(function () {
    return confirm('Вы действительно хотите удалить товар?');
});

// Скрипт добавления товара в вишлист
$(function ($) {
  $('.add_to_wishlist').click(function (event) {
    event.preventDefault();
    let heart_button = $(this).children();
    let url = $(this).attr('href');
    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': Cookies.get('csrftoken')
      },
    }).then(function (res) {
      if(res.status === 201) {
        heart_button.addClass('fa-heart');
        heart_button.removeClass('fa-heart-o');
      } else if(res.status === 204) {
        heart_button.addClass('fa-heart-o');
        heart_button.removeClass('fa-heart');
      }
    });
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

