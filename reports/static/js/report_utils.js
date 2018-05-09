$(function () {
    $("#main-dt").on("init.dt", function (e, settings) {
        const api = new $.fn.dataTable.Api(settings);
        api.columns().every(function () {
            const column = this;
            if (column.data().unique().length > 10) {
                return;
            }
            const select = $('<select><option value=""></option></select>')
                .appendTo($(column.footer()).empty())
                .on('change', function () {
                    let val = $.fn.dataTable.util.escapeRegex($(this).val());
                    column.search(val ? '^' + val + '$' : '', true, false).draw();
                });

            column.data().unique().sort().each(function (d, j) {
                select.append($("<option/>").val(d).text(d));
            });
        });
    });
});