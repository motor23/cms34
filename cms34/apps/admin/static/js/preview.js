// preview
$(window).addEvent('domready', function(){
    var a = $$('.navigation a[href="/preview/"]')[0];
    a.parentElement.addClass('active');

    $$('[data-preview]').each(function(block){
        var edit_url = block.get('data-preview-edit');
        var where = block.get('data-preview-where');
        var preview_buttons = new Element('div', {'class': "preview_buttons"});
        preview_buttons.inject(block, where);
        if(edit_url){
            var a = new Element('a', {'href': edit_url, 'html':'Редактировать'});
            a.inject(preview_buttons)
        }
    });
});
