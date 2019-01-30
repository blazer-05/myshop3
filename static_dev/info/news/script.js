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
let like = function (id) {
    $.ajax({
        url: "/news/like/",
        type: "POST",
        data: {
            pk: id,
        },
        success: (response) => {
            window.location = response
        },
        error: (response) => {
            console.log("False")
        }
    })
};

// Поставить лайк дизлайк
let dislike = function (id) {
    $.ajax({
        url: "/news/dislike/",
        type: "POST",
        data: {
            pk: id,
        },
        success: (response) => {
            window.location = response
        },
        error: (response) => {
            console.log("False")
        }
    })
};