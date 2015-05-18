var StreamSelect = new Class({
  // XXX name of class?
    Implements: [Options, Events],

    initialize: function(widget, options){
        this.setOptions(options);
        this.widget = widget;
        this.popup = new Popup();
    },

    show: function(){
        this.drawList();
        this.popup.show();
    },

    hide: function(){
        this.drawList();
        this.popup.hide();
    },
    typeOfElement: function(el) {
      try {
        return el.getElement('.field_type_name').getElement('a').innerHTML.trim();
      } catch (exc) {
        return 'error';
      }
    },
    filterFiles: function(elems) {
      var children = elems.getChildren();
      // This is bad, i know
      for (var i=0; i < children.length; i++) {
        if (this.typeOfElement(children[i]).toLocaleLowerCase() === 'файл') {
          children[i].destroy();
        }
      }
      return elems;
    },
    drawList: function(){
      this.popup.contentEl.empty();
      var elems = this.widget.getItemsDiv().clone();
      if (elems.getChildren().length === 0) {
        this.popup.adopt(new Element('div', {'html': 'Отсутствуют прикрепленные элементы'}));
      }
      else {
        if (this.options.hide_files) {
          elems = this.filterFiles(elems);
        }
        var container = new Element('table', {'class': 'w-popup-stream-select-items'});
        container.addEvent('click', function(e){
          e.stop();
          var row = e.target.tagName == 'TR'? e.target: e.target.getParent('tr.item');
          this.fireEvent('change', {'value': row.getElement('.field_id').get('text').trim()});
        }.bind(this));
        container.adopt(elems);
        container.getElements('.w-control-cell').destroy();
        container.getElements('a').set('href', 'javascript: void(0)');
      }
      this.popup.adopt(container);
      this.popup.onWindowResize();
    }
});

