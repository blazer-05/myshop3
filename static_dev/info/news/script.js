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
            url: "/news/like/",
            type: "POST",
            data: {
                pk: el.data('comment-id'),
            },
            success: function () {
                let el_counter = el.parent().find('.label-success')
                let count = parseInt(el_counter.text()) + 1
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
            url: "/news/dislike/",
            type: "POST",
            data: {
                pk: el.data('comment-id'),
            },
            success: function () {
                let el_counter = el.parent().find('.label-danger')
                let count = parseInt(el_counter.text()) + 1
                el_counter.text(count)
            }
        })
    }
})



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