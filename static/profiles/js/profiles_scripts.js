// Скрипт подписки/отписки на новости из личного кабинета.
jQuery(document).ready(function ($) {
  $('#TriSeaSuccess').on('change', function (el) {
    $.ajax({
      url: "/accounts/profile/subscribe/",
      type: "POST",
      data: {
        need_to_subscribe: $(this).is(":checked") ? '1' : '',
      },
    });
  });
});

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


