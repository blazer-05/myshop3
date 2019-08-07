
<!-- Скрипт чекбокса политики конфидециальности, если флаг не установле, то кнопка submit не активна! contact.html и signup.html -->
        //JavaScript
    // form.onchange = function(){
    //   var button = document.body.getElementsByClassName('btn')[0];
    //   if(button.disabled) button.disabled = false;
    //   else button.disabled = true;
    // }
    //
    // //Jquery
    // $('#form').on('change', function(){
    //   if($(this).is(':checked')) $('.btn').attr('disabled', false);
    //   else $('.btn').attr('disabled', true);
    // });


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