// Установка csrf_token
(function () {
    let csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });
})();

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
