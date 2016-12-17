$(function () {
    $('#greetings-modal').modal('show');
    $('#greetings-modal .dismiss-greetings').on('click', function() {
        $.post('/config/mensaje_de_bienvenida', {});
        $('#greetings-modal').modal('hide');
    });
});