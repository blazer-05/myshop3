// Установка csrf_token
(function () {
    let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });
})();


// Показать/скрыть форму ответа на коментарий - кнопка (reply)
let openForm = function (id) {
    $(`#${id}`).toggle()
}

// Скрыть форму ответа на комментарий - кнопка (close)
let closeForm = function (id) {
    $(`#${id}`).hide()
}

// Поставить лайк
$(document).ready(function () {
    like = function (el) {
         el = $(el)
        $.ajax({
            url: "/comments/like/",
            type: "POST",
            data: {
                pk: el.data('comment-id'),
            },
            success: function (data, textStatus, jqXHR ) {
                let i = jqXHR.status == 201 ? 1 : -1
                let el_counter = el.parent().find('.label-success')
                let count = parseInt(el_counter.text()) + i
                el_counter.text(count)
            }
        })
    }
})

// Поставить дизлайк
$(document).ready(function () {
    dislike = function (el) {
         el = $(el)
        $.ajax({
            url: "/comments/dislike/",
            type: "POST",
            data: {
                pk: el.data('comment-id'),
            },
            success: function (data, textStatus, jqXHR ) {
                let i = jqXHR.status == 201 ? 1 : -1
                let el_counter = el.parent().find('.label-danger')
                let count = parseInt(el_counter.text()) + i
                el_counter.text(count)
            }
        })
    }
})


// Скрипт обновления капчи (refresh)
$(document).ready(function() {
    // Add refresh button after field (this can be done in the template as well)
    // {#$('img.captcha').after(#}
    // {#        $('<a href="#void" class="captcha-refresh">Refresh</a>')#}
    // {#        );#}

    // Click-handler for the refresh-link
    $('.captcha-refresh').click(function(){
        var $form = $(this).parents('form');
        var url = location.protocol + "//" + window.location.hostname + ":"
                  + location.port + "/captcha/refresh/";

        // Make the AJAX-call
        $.getJSON(url, {}, function(json) {
            $form.find('input[name="captcha_0"]').val(json.key);
            $form.find('img.captcha').attr('src', json.image_url);
        });

        return false;
    });
});

// Подтверждение удаления комментария, id на кнопке Delete
$('#delete').click(function () {
    return confirm('Вы действительно хотите удалить комментарий?');
});


// Ошибка капчи при неправильном вводе кода капчи.
function submit_comment_form(event) {
  event.preventDefault();

  let formData = new FormData(event.target);
  let data = {};
  formData.forEach(function (value, key) {
    data[key] = value;
  });

  $.ajax({
    url: event.target.action,
    type: "POST",
    data: data,
    success: function (data, textStatus, jqXHR) {
      window.location.href = window.location.href
    },
    error: function (jqXHR, textStatus, errorThrown) {
      let json = jqXHR.responseJSON;

      let comment_form_errors_class = 'comment_form_errors';
      $(event.target).find('.'+comment_form_errors_class).remove();

      let labels = $(event.target).find('label');
      for (let index in labels) {
        let label = labels[index];

        if (label.htmlFor === undefined)
          continue;

        let field = label.htmlFor.replace('id_', '');
        if (json.hasOwnProperty(field)) {
          $('<span>')
            .addClass(comment_form_errors_class)
            .css('color', 'red')
            .text(' '+json[field].join(', '))
            .insertAfter($(label))
        }
      }
      $('.form_errors').append($('<span>')
        .addClass(comment_form_errors_class)
        .css('color', 'red')
        .text('Проверьте правильность данных'))

      $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
      });
    }
  });
}



// $(document).ready(function () {
//     like = function (el) {
//          el = $(el)
//         $.ajax({
//             url: "/news/like/",
//             type: "POST",
//             data: {
//                 pk: el.data('comment-id'),
//             },
//             success: function () {
//                 let el_counter = el.parent().find('.label-success')
//                 let count = parseInt(el_counter.text()) + 1
//                 el_counter.text(count)
//             }
//         })
//     }
// })




// $(document).ready(function () {
//     dislike = function (el) {
//          el = $(el)
//         $.ajax({
//             url: "/news/dislike/",
//             type: "POST",
//             data: {
//                 pk: el.data('comment-id'),
//             },
//             success: function () {
//                 let el_counter = el.parent().find('.label-danger')
//                 let count = parseInt(el_counter.text()) + 1
//                 el_counter.text(count)
//             }
//         })
//     }
// })


// let dislike = function (id) {
//     $.ajax({
//         url: "/news/dislike/",
//         type: "POST",
//         data: {
//             pk: id,
//         },
//         success: (response) => {
//             window.location = response
//         },
//         error: (response) => {
//             console.log("False")
//         }
//     })
// };



//  $(document).ready(function() {
//   $('#openModal').click();
//     $.ajax({
//         url: "/news/success/",
//         type: "POST",
//         // data: {
//         //     pk: id,
//         // },
//         // success: () => {
//         //     window.onload = response
//         // },
//         // error: (response) => {
//         //     console.log("False")
//         // }
//     })
// });

