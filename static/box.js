$(document).ready(function() {

    $("#CANDU-form").submit(function(event) {
        event.preventDefault(); //prevent default action
        var checked_reactors = [];
        var post_url = $(this).attr("action"); //get form action url
        var start_date = $('input[name="startDate"]')[0].value; //our date input has the name "date"
        var end_date = $('input[name="endDate"]')[0].value;
        $.each($("input[name='check[]']:checked"), function() {
            checked_reactors.push($(this).attr("id"));
        });
        var data = {
            reactors: checked_reactors,
            start: start_date,
            end: end_date
        };
        $.post(post_url, data, function(response) {
            $("#server-results").html(response);
        });
    });

    $(".parent").each(function(index) {
        var group = $(this).data("group");
        var parent = $(this);

        parent.change(function() { //"select all" change 
            $(group).prop('checked', parent.prop("checked"));
        });
        $(group).change(function() {
            parent.prop('checked', false);
            if ($(group + ':checked').length == $(group).length) {
                parent.prop('checked', true);
            }
        });
    });
});