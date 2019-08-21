
// вывод сообщений о подписке в модальном окне под формой подписки
$(document).ready(
  $('#subscribe_form').on('submit', function(event){
    event.preventDefault();
    let message_el = $('#subscribe_form_message');
    $.ajax({
      url: '/newsletter/subscribe/',
      type: 'post',
      data: $(this).serialize(),
      success: function (data, textStatus, jqXHR) {
        message_el.removeClass('alert-danger')
        message_el.addClass('alert-success')
        message_el.text(data.message)
      },
      error: function (jqXHR, textStatus, errorThrown) {
        message_el.removeClass('alert-success')
        message_el.addClass('alert-danger')
        message_el.text(jqXHR.responseJSON.message)
      }
    })
  })
);