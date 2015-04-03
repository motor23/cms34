Blocks.register('tree_expand', function(container){
    var table = container.getParent('table.items')
    if(!table){
        return;
    }
    var tree = table.retrieve('tree', []);

    function TreeElement(tree, el){
        this.tree = tree;
        this.open_button = el.getElement('.tree_expand_open_button'); 
        this.close_button = el.getElement('.tree_expand_close_button'); 
        this.has_childs = el.get('data-childs');
        this.level = parseInt(el.get('data-level'));
        this.id = el.get('data-id');
        this.parent_id = el.get('data-parent');
        this.td = el.getParent('td');
        this.tr = this.td.getParent('tr.item');
        this.childs = []
        this.parent_item = null;
        this.hidden = false;
        this.closed = false;
        this.td.setStyle('padding-left', (this.level-1) * 40 + 10);
        this.tree.each(function(item){
            if(item.id==this.parent_id){
                item.childs.push(this);
                this.parent_item = item;
            }
        }, this);
        this.show = function(){
            this.hidden = false;
            if(!this.closed)
                this.childs.each(function(item){item.show()});
            this.tr.setStyle('display', 'table-row');
        }
        this.hide = function(){
            this.hidden = true;
            this.childs.each(function(item){item.hide()});
            this.tr.setStyle('display', 'none');
        }
        this.open = function(){
            this.closed = false;
            if(!this.has_childs)
                return;
            this.childs.each(function(item){item.show()});
            localStorage.setItem('tree-open-'+this.id, '1');
            el.removeClass('closed');
            el.addClass('opened');
        }
        this.close = function(){
            this.closed = true;
            if(!this.has_childs)
                return;
            this.childs.each(function(item){item.hide()});
            localStorage.setItem('tree-open-'+this.id, '');
            el.removeClass('opened');
            el.addClass('closed');
        }
        this.open_button.addEvent('click', this.open.bind(this));
        this.close_button.addEvent('click', this.close.bind(this));
        if(this.has_childs){
            var opened = localStorage.getItem('tree-open-'+this.id);
            if(opened){
                this.open();
            }else{
                this.close();
            }
        }
        if(this.parent_item&&
           (this.parent_item.closed||this.parent_item.hidden)){
            this.hide();
        }
        tree.push(this);
    }
    var tree_element = new TreeElement(tree, container);
});

