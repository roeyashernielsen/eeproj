/**
 * Created by roeya on 18/06/2016.
 */
$(document).ready(function(){
    var next = 1;
    $(".add-more").click(function(e){
        e.preventDefault();
        var addto = "#field" + next;
        var removefrom = "#field" + (next);
        next = next + 1;
        var newIn = '<select class="element select medium"  id="element_' + next + '" name="element_' + next + '" ><option value="" selected="selected"></option><option value="1" >First option</option><option value="2" >Second option</option> <option value="3" >Third option</option></select><input autocomplete="off" class="input form-control" id="field' + next + '" name="field' + next + '" type="text"> <p class="guidelines" id="guide_1"><small>Please select open rule</small></p>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >-</button></div><div id="field">';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(removefrom).after(removeButton);
        $("#field" + next).attr('data-source',$(addto).attr('data-source'));
        $("#element_" + next).attr('data-source',$(addto).attr('data-source'));
        $("#count").val(next);

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#field" + fieldNum;
                var elementID = "#element_" + fieldNum;
                $(this).remove();
                $(fieldID).remove();
                $(elementID).remove();
            });
    });
});