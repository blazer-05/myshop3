
// Показать и скрыть форму добавления отзыва, (openForm - в шаблоне review.html) и
// (closeForm - в шаблоне review.html)

    let openForm = function () {
    $('.reviews').show()
    $('.btn-info').toggleClass("btn-hide").hide()
}

    let closeForm = function () {
    $('.reviews').hide()
    $('.btn-info').toggleClass("btn-show").show()
}




// Скрипт привью загрузки изображения в форме добавления отзыва, шаблон create_review.html
function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah')
                    .attr('src', e.target.result);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }


// Скрипт выбора количества звезд в форме создания отзыва
jQuery(document).ready(function ($) {

    let raiting_field = $("#id_rating");
    raiting_field.hide();
    $(".btnrating").on('click', (function (e) {
        let previous_value = raiting_field.val();
        let selected_value = $(this).attr("data-attr");
        raiting_field.val(selected_value);
        $('.selected-rating').text($("#id_rating option:selected" ).text())

        for (i = 1; i <= selected_value; ++i) {
            $("#rating-star-" + i).toggleClass('btn-warning');
            $("#rating-star-" + i).toggleClass('btn-default');
        }

        for (ix = 1; ix <= previous_value; ++ix) {
            $("#rating-star-" + ix).toggleClass('btn-warning');
            $("#rating-star-" + ix).toggleClass('btn-default');
        }

    }));


});


// Ошибка капчи при неправильном вводе кода капчи - форма отзывов.
function submit_review_form(event) {
  event.preventDefault();

  let formData = new FormData(event.target);
  let data = {};
  formData.forEach(function (value, key) {
    data[key] = value;
  });

  $.ajax({
    url: event.target.action,
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (data, textStatus, jqXHR) {
      window.location.href = window.location.href
    },
    error: function (jqXHR, textStatus, errorThrown) {
      let json = jqXHR.responseJSON;

      let review_form_errors_class = 'review_form_errors';
      $(event.target).find('.'+review_form_errors_class).remove();

      let labels = $(event.target).find('label');
      for (let index in labels) {
        let label = labels[index];

        if (label.htmlFor === undefined)
          continue;

        let field = label.htmlFor.replace('id_', '');
        if (json.hasOwnProperty(field)) {
          $('<span>')
            .addClass(review_form_errors_class)
            .css('color', 'red')
            .text(' '+json[field].join(', '))
            .insertAfter($(label))
        }
      }
      $('.form_errors').append($('<span>')
        .addClass(review_form_errors_class)
        .css('color', 'red')
        .text('Проверьте правильность данных'))

      $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
      });
    }
  });
}


// Скрипт кнопки close в шаблоне edit_review.html
$("#close").click(function(e) {
  e.preventDefault();
  location.href = "/";
});


// Подтверждение удаления комментария, id на кнопке Delete
$('#review_delete').click(function () {
    return confirm('Вы действительно хотите удалить отзыв?');
});