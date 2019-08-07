
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


