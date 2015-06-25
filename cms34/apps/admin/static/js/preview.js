// preview
$(window).ready(function(){
    var a = $('.navigation a[href="/preview/"]');
    a.parent('li').addClass('active');

    var blocks = $('[data-preview]');
    blocks.each(function(index, block){
        var preview_buttons = $('<div class="preview_buttons"></div>');
        $(block).append(preview_buttons);
        var edit_url = $(block).data('preview-edit');
        if(edit_url){
            preview_buttons.append($('<a href="'+edit_url+'">Редактировать</a>'))
        }
    });
});
