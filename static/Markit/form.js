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

        var li3 = document.getElementById('open_li_3_1_1'),
        cloneli3 = li3.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli3.id = "li_3_" +clauseNum+ "_" + next;
        $(cloneost).after(cloneli3);
        
        var li7 = document.getElementById('open_li_7_1_1'),
        cloneli7 = li7.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli7.id = "open_li_7_" +clauseNum+ "_" + next;
        $(cloneli3).after(cloneli7);

        var li4 = document.getElementById('open_li_4_1_1'),
        cloneli4 = li4.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli4.id = "open_li_4_" +clauseNum+ "_" + next;
        $(cloneli7).after(cloneli4);

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
        var addto = "#open_li_6";
        next2 = next2 + 1;

        var osc = document.getElementById('osc1'),
        cloneosc = osc.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneosc.id = "osc" + next2;
        cloneosc.innerHTML = "Start clause " + next2;
        $(addto).before(cloneosc);

        var ul = document.getElementById('oul1'),
        cloneul = ul.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneul.id = "oul_" + next2;
        $(cloneosc).after(cloneul);

        var oec = document.getElementById('oec1'),
        cloneoec = oec.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneoec.id = "oec" + next2;
        cloneoec.innerHTML = "End clause " + next2;
        $(cloneul).after(cloneoec);
        
    });
});

$(document).ready(function(){
    var next = 1;
    $(".add-more-close-terms").click(function(e){
        e.preventDefault();
        var clauseNum = this.id.charAt(this.id.length-1);
        var addto = "#cet_" + clauseNum + "_" + next;
        next = next + 1;

        var cst = document.getElementById('cst_1_1'),
        clonecst = cst.cloneNode(true); // true means clone all childNodes and all event handlers
        clonecst.id = "cst_" +clauseNum+ "_" + next;
        clonecst.innerHTML = "Start term " + next;
        $(addto).after(clonecst);

        var li3 = document.getElementById('close_li_3_1_1'),
        cloneli3 = li3.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli3.id = "close_li_3_" +clauseNum+ "_" + next;
        $(clonecst).after(cloneli3);

        var li7 = document.getElementById('close_li_7_1_1'),
        cloneli7 = li7.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli7.id = "close_li_7_" +clauseNum+ "_" + next;
        $(cloneli3).after(cloneli7);

        var li4 = document.getElementById('close_li_4_1_1'),
        cloneli4 = li4.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneli4.id = "close_li_4_" +clauseNum+ "_" + next;
        $(cloneli7).after(cloneli4);

        var cet = document.getElementById('cet_1_1'),
        clonecet = cet.cloneNode(true); // true means clone all childNodes and all event handlers
        clonecet.id = "cet_" +clauseNum+ "_" + next;
        clonecet.innerHTML = "End term " + next;
        $(cloneli4).after(clonecet);
    });
});

$(document).ready(function(){
    var next2 = 1;
    $(".add-more-close-clause").click(function(e){
        e.preventDefault();
        var addto = "#close_li_6";
        next2 = next2 + 1;

        var csc = document.getElementById('csc1'),
        clonecsc = csc.cloneNode(true); // true means clone all childNodes and all event handlers
        clonecsc.id = "csc" + next2;
        clonecsc.innerHTML = "Start clause " + next2;
        $(addto).before(clonecsc);

        var ul = document.getElementById('cul1'),
        cloneul = ul.cloneNode(true); // true means clone all childNodes and all event handlers
        cloneul.id = "cul_" + next2;
        $(clonecsc).after(cloneul);

        var cec = document.getElementById('cec1'),
        clonecec = cec.cloneNode(true); // true means clone all childNodes and all event handlers
        clonecec.id = "cec" + next2;
        clonecec.innerHTML = "End clause " + next2;
        $(cloneul).after(clonecec);

    });
});