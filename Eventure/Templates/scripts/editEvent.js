$(document).ready(function() {
    $('.add-item').click(function(ev) {
        ev.preventDefault();
        var count = $('#items-form-container').children().length;
        var tmplMarkup = $('#item-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);

        $('tbody#items-form-container').append(compiledTmpl);
        $('tbody#items-form-container [id^=item-]').addClass("itemTable");

        // update form count
        $('#id_item-TOTAL_FORMS').attr('value', count+1);
        addItemBootStrap(); // Add BS to new forms
    });
});

$(document).ready(function() {
    $('.add-invitee').click(function(ev) {
        ev.preventDefault();
        var count = $('#invitees-form-container').children().length;
        var tmplMarkup = $('#invitee-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);

        $('div#invitees-form-container').append(compiledTmpl);

        $('div#invitees-form-container [id^=invitee-]').addClass("inviteTable");

        console.log(compiledTmpl);

        // update form count
        $('#id_invitee-TOTAL_FORMS').attr('value', count+1);
        addEmailBootStrap();
    });
});

var itemTable = $('.itemTable');

// Delete button
itemTable.on("click", "a.deleteElement", function(ev) {
    ev.preventDefault();
    console.log("Hello");
    $(this).parent().parent().children("td").hide();
});

// Undo button
itemTable.on("click", "a.redoElement", function(ev) {
    ev.preventDefault();

    $(this).parent().parent().children("td").show();

});

// Toggle Delete/Undo button
itemTable.on("click", "a.modifyItemList", function(ev) {
    $(this).parent().children().toggle();
});


// Start up
$(document).ready(function (){
    addEmailBootStrap();
    addItemBootStrap();
    addItemTableBootStrap();
});

function addEmailBootStrap(){
    $('[id$="email"]').each(function(index) {
        $(this).addClass("form-control");
    });

    $('.inviteTable').each(function(){
       $(this).addClass('form-inline');
    });
}

function addItemBootStrap(){
    $('[id$="itemName"]').each(function(index) {
        $(this).addClass("form-control");
    });

    $('[id$="amount"]').each(function(index) {
        $(this).addClass("form-control itemAmountInput");
    });
    $('.itemTable ').each(function(){
       $(this).addClass('form-inline');
    });
}


function addItemTableBootStrap(){
    $('td input[id$="name"]').each(function(index) {
        $(this).addClass("form-control");
    });

}


