$(document).ready(function() {
    $(".input-key").keyup(function() {
        if ($(this).val().length == $(this).attr("maxlength")) {
            $(this).next('.input-key').focus();
        }
    });
});