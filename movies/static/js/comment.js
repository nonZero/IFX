console.log("START");

$(function () {
    console.log("READY START");
    // TODO: disable button if no content is available

    $("#send-form").click(function () {
        console.log('click');
        // const url = $("#comment-form").attr('action');
        const url = "";
        console.log(url);
        const data = {
            content: $("#id_content").val()
        };
        // TODO: validate data
        // See also: jquery-form plugin
        console.log(data);
        $("#send-form").prop('disabled', true);
        $.post(url, data).done(function (resp) {
            $("#comments").children().first().after(resp);
            $("#id_content").val('').focus();
            $("#send-form").prop('disabled', false);
        }).fail(function (jqxhr, resp) {
            var errors = jqxhr.responseJSON;
            console.log(errors);
            // TODO: show errors
            debugger;
        });
        return false;
    });

    console.log("READY END");
});

console.log("END");