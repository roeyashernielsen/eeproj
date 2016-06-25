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
        var newIn = '<select class="element select medium"  id="element_' + next + '" name="element_' + next + '" ><option value="" selected="selected"></option><option value="1" >First option</option><option value="2" >Second option</option> <option value="3" >Third option</option></select><input autocomplete="off" class="input form-control" id="field' + next + '" name="field' + next + '" type="text">';
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

        var ost = document.getElementById('ost_1_1'),
        cloneost = ost.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneost.id = "ost_" +clauseNum+ "_" + next;
        cloneost.innerHTML = "Start term " + next;
        $(addto).after(cloneost);

        var li3 = document.getElementById('li_3_1_1'),
        cloneli3 = li3.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli3.id = "li_3_" +clauseNum+ "_" + next;
        $(cloneost).after(cloneli3);

        var li4 = document.getElementById('li_4_1_1'),
        cloneli4 = li4.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli4.id = "li_4_" +clauseNum+ "_" + next;
        $(cloneli3).after(cloneli4);

        var oet = document.getElementById('oet_1_1'),
        cloneoet = oet.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneoet.id = "oet_" +clauseNum+ "_" + next;
        cloneoet.innerHTML = "End term " + next;
        $(cloneli4).after(cloneoet);
    });
});

$(document).ready(function(){
    var next2 = 1;
    $(".add-more-open-clause").click(function(e){
        e.preventDefault();
        var addto = "#li_6";
        next2 = next2 + 1;

        var osc = document.getElementById('osc1'),
        cloneosc = osc.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneosc.id = "osc" + next2;
        cloneosc.innerHTML = "Start clause " + next2;
        $(addto).before(cloneosc);

        var ul = document.getElementById('ul1'),
        cloneul = ul.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneul.id = "ul_" + next2;
        $(cloneosc).after(cloneul);

        var oec = document.getElementById('oec1'),
        cloneoec = oec.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneoec.id = "oec" + next2;
        cloneoec.innerHTML = "End clause " + next2;
        $(cloneul).after(cloneoec);
        
    });
});

