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
        var newIn = '<select class="element select medium"  id="element_' + next + '" name="element_' + next + '" ><option value="" selected="selected"></option><option value="1" >First option</option><option value="2" >Second option</option> <option value="3" >Third option</option></select><input autocomplete="off" class="input form-control" id="field' + next + '" name="field' + next + '" type="text"> ';
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

$(document).ready(function(){
    var next = 1;
    $(".add-more-open-terms").click(function(e){
        e.preventDefault();
        var addto = "#et" + next;
        var removefrom = "#et" + (next);
        next = next + 1;
        var newIn = '<p id="st' + next + '">Start term</p><li id="li_3_' + next + '"><div><span> <label class="description" for="element_3_' + next + '">Name</label> <select class="element select medium" id="element_3_' + next + '" name="element_3_' + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_6_' + next + '">Period </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Shifting </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li> <li id="li_4_' + next + '" > <div> <span> <label class="description" for="element_3_' + next + '">Name</label> <select class="element select medium" id="element_3_' + next + '" name="element_3_' + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_6_' + next + '">Period </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Shifting </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Value</label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li><p id="et' + next + '">End term</p>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >Remove term</button>';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(removefrom).after(removeButton);

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#et" + fieldNum;
                var fieldDD = "#st" + fieldNum;
                var elementID = "#li_3_" + fieldNum;
                var elementDD = "#li_4_" + fieldNum;
                $(this).remove();
                $(fieldDD).remove();
                $(fieldID).remove();
                $(elementID).remove();
                $(elementDD).remove();
            });
    });
});

$(document).ready(function(){
    var next = 1;
    $(".add-more-close-terms").click(function(e){
        e.preventDefault();
        var addto = "#cet" + next;
        var removefrom = "#cet" + (next);
        next = next + 1;
        var newIn = '<p id="cst' + next + '">Start term</p><li id="li_6_' + next + '"><div><span> <label class="description" for="element_3_' + next + '">Name</label> <select class="element select medium" id="element_3_' + next + '" name="element_3_' + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_6_' + next + '">Period </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Shifting </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li> <li id="li_7_' + next + '" > <div> <span> <label class="description" for="element_3_' + next + '">Name</label> <select class="element select medium" id="element_3_' + next + '" name="element_3_' + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_6_' + next + '">Period </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Shifting </label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_6_' + next + '">Value</label> <input id="element_6_' + next + '" name="element_6_' + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li><p id="cet' + next + '">End term</p>';
        var newInput = $(newIn);
        var removeBtn = '<button id="remove' + (next - 1) + '" class="btn btn-danger remove-me" >Remove term</button>';
        var removeButton = $(removeBtn);
        $(addto).after(newInput);
        $(removefrom).after(removeButton);

            $('.remove-me').click(function(e){
                e.preventDefault();
                var fieldNum = this.id.charAt(this.id.length-1);
                var fieldID = "#cet" + fieldNum;
                var fieldDD = "#cst" + fieldNum;
                var elementID = "#li_6_" + fieldNum;
                var elementDD = "#li_7_" + fieldNum;
                $(this).remove();
                $(fieldDD).remove();
                $(fieldID).remove();
                $(elementID).remove();
                $(elementDD).remove();
            });
    });
});