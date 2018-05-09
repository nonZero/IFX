$(function () {
    $(".set-movie").click(function (e, settings) {
        const el = $(this);
        const td = el.closest('td');
        const url = el.data('url');
        td.html('<span class="fas fa-spinner fa-spin"></span>');
        $.post(url).done(resp => {
            td.html(resp.html);
        }).fail(resp => {
            td.html('<span class="fa fa-exclamation-triangle fa-4x text-danger"></span>');
            console.error(resp);
        });
    });
});