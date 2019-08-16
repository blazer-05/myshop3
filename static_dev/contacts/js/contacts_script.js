

// Вывод и отправка формы обратного звонка в модальном окне

$('#back_call').on('shown.bs.modal', function () {
  let container = $(this).find('.modal-back_call');
  if(container.text().trim() === '') {
    $.ajax({
      type: "GET",
      url: "/contact/backcall/",
    }).done(function (data) {
      container.html(data);
      refreshCaptcha(container.find('.captcha-refresh'));
      bind_form_submit(container.find('form'))
    });
  }
})

function refreshCaptcha(element) {
  element.click(function () {
    var $form = $(this).parents('form');
    var url = location.protocol + "//" + window.location.hostname + ":"
      + location.port + "/captcha/refresh/";

    // Make the AJAX-call
    $.getJSON(url, {}, function (json) {
      $form.find('input[name="captcha_0"]').val(json.key);
      $form.find('img.captcha').attr('src', json.image_url);
    });

    return false;
  });
}

function bind_form_submit(form) {
  form.on('submit', (function (event) {
    event.preventDefault();
    let container = $(this).closest('.modal-back_call');
    let data = {};
    $.each(form.serializeArray(), function (i, v) {
      data[v.name] = v.value;
    });
    $.ajax({
      type: "POST",
      url: "/contact/backcall/",
      data: data
    }).done(function (data) {
      container.html(data);
      refreshCaptcha(container.find('.captcha-refresh'));
      bind_form_submit(container.find('form'))
    });
    return false;
  }))
}