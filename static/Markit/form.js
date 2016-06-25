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
        var clauseNum = this.id.charAt(this.id.length-1);
        var addto = "#oet_" + clauseNum + "_" + next;
        next = next + 1;
        var newIn = '<p id="ost_'+ clauseNum+ "_" + next + '" style="margin-left: 50px;">Start term ' + next + '</p><li id="li_3_'+ clauseNum+ "_" + next + '" style="margin-left: 50px;"><div><span> <label class="description" for="element_3_1_'+ clauseNum+ "_" + next + '">Name</label> <select class="element select medium" id="element_3_1_'+ clauseNum+ "_" + next + '" name="element_3_1_'+ clauseNum+ "_" + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_3_2_'+ clauseNum+ "_" + next + '">Period </label> <input id="element_3_2_'+ clauseNum+ "_" + next + '" name="element_3_2_'+ clauseNum+ "_" + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_3_3_'+ clauseNum+ "_" + next + '">Shifting </label> <input id="element_3_3_'+ clauseNum+ "_" + next + '" name="element_3_3_'+ clauseNum+ "_" + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li> <li id="li_4_'+ clauseNum+ "_" + next + '" style="margin-left: 50px;"> <div> <span> <label class="description" for="element_4_1_'+ clauseNum+ "_" + next + '">Name</label> <select class="element select medium" id="element_4_1_'+ clauseNum+ "_" + next + '" name="element_4_1_'+ clauseNum+ "_" + next + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_4_2_'+ clauseNum+ "_" + next + '">Period </label> <input id="element_4_2_'+ clauseNum+ "_" + next + '" name="element_4_2_'+ clauseNum+ "_" + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_3_'+ clauseNum+ "_" + next + '">Shifting </label> <input id="element_4_3_'+ clauseNum+ "_" + next + '" name="element_4_3_'+ clauseNum+ "_" + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_4_'+ clauseNum+ "_" + next + '">Value</label> <input id="element_4_4_'+ clauseNum+ "_" + next + '" name="element_4_4_'+ clauseNum+ "_" + next + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li><p id="oet_'+ clauseNum+ "_" + next + '" style="margin-left: 50px;">End term ' + next + '</p>';
        var newInput = $(newIn);
        $(addto).after(newInput);
    });
});

$(document).ready(function(){
    var next = 1;
    $(".add-more-open-clause").click(function(e){
        e.preventDefault();
        var addto = "#li_6";
        next = next + 1;
        var newIn = '<ul id="ul' + next + '"><h3 id="osc_' + next + ' ">Start clause ' + next + '</h3><p id="ost_'+ next + "_" + 1 + '" style="margin-left: 50px;">Start term 1</p><li id="li_3_'+ next+ "_" + 1 + '" style="margin-left: 50px;"><div><span> <label class="description" for="element_3_1_'+ next + "_" + 1 + '">Name</label> <select class="element select medium" id="element_3_1_'+ next + "_" + 1 + '" name="element_3_1_'+ next + "_" + 1 + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_3_2_'+ next + "_" + 1 + '">Period </label> <input id="element_3_2_'+ next + "_" + 1 + '" name="element_3_2_'+ next + "_" + 1 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_3_3_'+ next + "_" + 1 + '">Shifting </label> <input id="element_3_3_'+ next + "_" + 1 + '" name="element_3_3_'+ next + "_" + 1 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li> <li id="li_4_'+ next + "_" + 1 + '" style="margin-left: 50px;"> <div> <span> <label class="description" for="element_4_1_'+ next + "_" + 1 + '">Name</label> <select class="element select medium" id="element_4_1_'+ next + "_" + 1 + '" name="element_4_1_'+ next + "_" + 1 + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_4_2_'+ next + "_" + 1 + '">Period </label> <input id="element_4_2_'+ next + "_" + 1 + '" name="element_4_2_'+ next + "_" + 1 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_3_'+ next + "_" + 1 + '">Shifting </label> <input id="element_4_3_'+ next + "_" + 1 + '" name="element_4_3_'+ next + "_" + 1 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_4_'+ next + "_" + 1 + '">Value</label> <input id="element_4_4_'+ next + "_" + 1 + '" name="element_4_4_'+ next + "_" + 1 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li><p id="oet_'+ next + "_" + 1 + '" style="margin-left: 50px;">End term 1</p><li id="li_5_' + next + '" style="margin-left: 50px;"><button id="OR' + next + '" class="btn btn-danger add-in-clause" type="button">OR</button></li><h3 id="osc_' + next + ' ">End clause ' + next + '</h3></ul>';
        var newInput = $(newIn);
        $(addto).before(newInput);

        var next2 = 1
        $(".add-in-clause").click(function(e) {
                e.preventDefault();
                var clauseNum = this.id.charAt(this.id.length - 1);
                var addto = "#oet_" + clauseNum + "_" + next2;
                next2 = next2 + 1;
                var newIn = '<p id="ost_' + clauseNum + "_" + next2 + '" style="margin-left: 50px;">Start term ' + next2 + '</p><li id="li_3_' + clauseNum + "_" + next2 + '" style="margin-left: 50px;"><div><span> <label class="description" for="element_3_1_' + clauseNum + "_" + next2 + '">Name</label> <select class="element select medium" id="element_3_1_' + clauseNum + "_" + next2 + '" name="element_3_1_' + clauseNum + "_" + next2 + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_3_2_' + clauseNum + "_" + next2 + '">Period </label> <input id="element_3_2_' + clauseNum + "_" + next2 + '" name="element_3_2_' + clauseNum + "_" + next2 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_3_3_' + clauseNum + "_" + next2 + '">Shifting </label> <input id="element_3_3_' + clauseNum + "_" + next2 + '" name="element_3_3_' + clauseNum + "_" + next2 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li> <li id="li_4_' + clauseNum + "_" + next2 + '" style="margin-left: 50px;"> <div> <span> <label class="description" for="element_4_1_' + clauseNum + "_" + next2 + '">Name</label> <select class="element select medium" id="element_4_1_' + clauseNum + "_" + next2 + '" name="element_4_1_' + clauseNum + "_" + next2 + '"> <option value="" selected="selected"></option> <option value="1" >First option</option> <option value="2" >Second option</option> <option value="3" >Third option</option> </select> </span> <span> <label class="description" for="element_4_2_' + clauseNum + "_" + next2 + '">Period </label> <input id="element_4_2_' + clauseNum + "_" + next2 + '" name="element_4_2_' + clauseNum + "_" + next2 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_3_' + clauseNum + "_" + next2 + '">Shifting </label> <input id="element_4_3_' + clauseNum + "_" + next2 + '" name="element_4_3_' + clauseNum + "_" + next2 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> <span> <label class="description" for="element_4_4_' + clauseNum + "_" + next2 + '">Value</label> <input id="element_4_4_' + clauseNum + "_" + next2 + '" name="element_4_4_' + clauseNum + "_" + next2 + '" class="element text medium" type="text" maxlength="255" value=""/> </span> </div> </li><p id="oet_' + clauseNum + "_" + next2 + '" style="margin-left: 50px;">End term ' + next2 + '</p>';
                var newInput = $(newIn);
                $(addto).after(newInput);
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

