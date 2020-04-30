$(document).ready(function() {

    function get_date(date_str) {
        var parts = date_str.split('/');
        return new Date(parts[2], parts[0] - 1, parts[1]);
    };

    function validate_input(start, end, reactors) {
        var today = new Date();
        var min_date = get_date('05/01/2019');
        var start_date = get_date(start);
        var end_date = get_date(end);

        if (reactors.length < 1) {
            return 'You must select at least one reactor from the list.';
        } else if (start_date > end_date) {
            return 'The start date must the same or less than the end date.';
        } else if (start_date < min_date) {
            return 'Sorry, data is only avalible from May, 1st 2019 onward. Please select a start date that is on or after May 1st, 2019';
        } else if (today <= end_date) {
            return 'Sorry, we aren\'t able to predict the future yet. Please select an end date prior to today\'s date.';
        } else {
            return true;
        }
    };

    $("#CANDU-form").submit(function(event) {
        event.preventDefault(); //prevent default action
        var checked_reactors = [];
        var post_url = $(this).attr("action"); //get form action url
        var start = $('input[name="startDate"]')[0].value;
        var end = $('input[name="endDate"]')[0].value;
        $.each($("input[name='check[]']:checked"), function() {
            checked_reactors.push($(this).attr("id"));
        });
        validation = validate_input(start, end, checked_reactors);
        if (validation === true) {
            var data = {
                reactors: checked_reactors,
                start: start,
                end: end
            };
            $.post(post_url, data, function(response) {
                window.location.href = '/results';
                localStorage.setItem('data', JSON.stringify(response));
            });
        } else {
            alert(validation);
        }
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

    $(".date").hover(function() {
        var start_date = $('input[name="startDate"]');
        var end_date = $('input[name="endDate"]');
        var container = $('.bootstrap-iso form').length > 0 ? $('.bootstrap-iso form').parent() : "body";
        var options = {
            format: 'mm/dd/yyyy',
            container: container,
            todayHighlight: true,
            autoclose: true
        };
        start_date.datepicker(options);
        end_date.datepicker(options);
    });
});