function createURL(href){
  var a = document.createElement('a');
  a.href = href;
  a.qs_get = function(){
      var result = {};
      query = this.search;
      if(query[0]=='?')
          query=query.substr(1);
      var vars = query.split('&');
      for (var i = 0; i < vars.length; i++) {
          var pair = vars[i].split('=');
          if(pair[0])
              result[decodeURIComponent(pair[0])]=decodeURIComponent(pair[1]);
      }
      return result;
  }

  a.set_search = function(q){
    var qs = Object.toQueryString(q);
    this.search = (qs && qs!='?') ? '?' + qs : '';
  }

  a.qs_set = function(obj){
    var q = this.qs_get();
    Object.append(q, obj);
    this.set_search(q)
  }

  a.qs_del= function(keys){
    var q = this.qs_get();
    q = Object.filter(q, function(value, key){
      return !keys.contains(key);
    });
    this.set_search(q);
  }

  a.eq = function(other){
      if((this.origin!=other.origin)||(this.pathname!=other.pathname))
          return false;
      var this_query = this.qs_get();
      var other_query = other.qs_get();
      if(Object.keys(this_query).length!=Object.keys(other_query).length)
          return false;
      return Object.every(Object.keys(this_query), function(key){
        return this_query[key]==other_query[key]
      })
  }
  return a;
}


var TabSelect = new Class ({

    Implements: Options,

    options: {
      inject_to: null, //css class or html element
      el: null
    },

    initialize: function(el, options){
      this.el = $(el);
      this.setOptions(options);

      this.el.getParent('.form-row').addClass('hide');
      var inject_to = this.options.inject_to;
      if(typeof(this.options.inject_to) == 'string'){
        inject_to = this.el.getParent('.content').getElement('.'+this.options.inject_to);
      }
      this.container = new Element('div').inject(inject_to);
      this.setup();
      
      $$('.js-button-add').addEvent('click', function(e){
          e.stop();
          var popup = new Popup('add');
          popup.setTitle('Создать');
          this.el.getChildren('option').each(function(el, index){
              if(!index)
                  return;
              var url = createURL(e.target.href);
              url.qs_set({type:el.value});
              var a = Element('a', {
                  html: el.innerHTML,
                  href: url.href,
              });
              var p = Element('p');
              a.inject(p)
              p.inject(popup.contentEl);
          });
          popup.show()
      }.bind(this));
 
    },

    setup: function(){
      this.el.getChildren('option').each(function(option) {   
        var tab = new Element('button', {
          html: option.innerHTML
        });
        if (option.getProperty('selected')) {
          tab.addClass('selected');
          if (this.options['option_hook_'+option.value]){
            eval(this.options['option_hook_'+option.value]);
          }
        }

        tab.addEventListener('click', function(e) {
          e.preventDefault(); e.stopPropagation();
          this.container.getChildren('button').removeClass('selected');
          tab.addClass('selected');
          option.setProperty('selected', true);
          this.submit();
        }.bind(this));
        tab.inject(this.container);
      }.bind(this), false);
    },

    submit: function() {
      this.el.getParent('form').retrieve('submitFilter')();
    }

  });

  Blocks.register('tab-select', function(el){
    new TabSelect(el.getElement('select'), JSON.parse(el.dataset.config));
  });
