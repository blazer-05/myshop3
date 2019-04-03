// Показать и скрыть форму добавления отзыва, (openForm - в шаблоне review.html) и
// (closeForm - в шаблоне add_form.html)

    let openForm = function () {
    $('.reviews').show()
}

    let closeForm = function () {
    $('.reviews').hide()
}



// Скрипт привью загрузки изображения в форме добавления отзыва, шаблон add_form.html
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