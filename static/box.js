$(document).ready(function(){
    $("button").click(function(){
        var reactors = [];
        $.each($("input[name='check[]']:checked"), function(){
            reactors.push($(this).attr("id"));
        });
        var start_date=$('input[name="startDate"]'); //our date input has the name "date"
        var end_date=$('input[name="endDate"]');
        var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
        var options={
        format: 'mm/dd/yyyy',
        container: container,
        todayHighlight: true,
        autoclose: true,
        };
        start_date.datepicker(options);
        end_date.datepicker(options);
    });

    $(".parent").each(function(index){
        var group = $(this).data("group");
        var parent = $(this);
    
        parent.change(function(){  //"select all" change 
             $(group).prop('checked', parent.prop("checked"));
        });
        $(group).change(function(){ 
            parent.prop('checked', false);
            if ($(group+':checked').length == $(group).length ){
                parent.prop('checked', true);
            }
        });
    });
});



