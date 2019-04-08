// Показать и скрыть форму добавления отзыва, (openForm - в шаблоне review.html) и
// (closeForm - в шаблоне create_review.html)

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

    $(".btnrating").on('click', (function (e) {

        var previous_value = $("#selected_rating").val();

        var selected_value = $(this).attr("data-attr");
        $("#selected_rating").val(selected_value);

        $(".selected-rating").empty();
        $(".selected-rating").html(selected_value);

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