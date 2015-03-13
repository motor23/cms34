var PopupCommand = Object({
    widgets: {},
    exec:  function(composer, command, value){
        if(!this.widgets[value]){
            this.widgets[value] = this.getWidget(composer, 
                                                 this.getFormId(composer), value);
        }
        this.widgets[value].show();
    },
    getWidget: function(composer, formId, name){
        var pss = $(formId + '-' + name).retrieve('widget');
        var widget = new StreamSelect(pss);
        widget.addEvent('change', function(e){
            widget.hide();
            // console.log('event-change', e);
            this.insert(composer, name, e.value);
        }.bind(this));
        return widget;
    },
    getFormId: function(composer){
        var textarea = composer.textarea.element;
        return textarea.getParent('form').id;
    },
    insert: function(composer, name, id){
    }
});

(function(wysihtml5) {
  var LinkPlugin = {

      getWidget: function(formId){
          var fieldlist = $(formId + '-' + this.widgetName).retrieve('widget');
          return new PopupFieldListSelect(fieldlist);
      },

      _init: function(composer){
        var textarea = composer.textarea.element;
        if (! textarea.retrieve(this.widgetName)){
          var widget = this.getWidget(textarea.getParent('form').get('id'));

          widget.addEvent('change', function(e){
            composer.commands.exec(this.commandName, e.value);
          }.bind(this));
          textarea.store(this.widgetName, widget);
        }
        return textarea.retrieve(this.widgetName);
      },

      tagName: 'ASIDE',
      widgetName: 'links_blocks', 
      commandName: 'doclink',
      // XXX show front version from front widget
      url: '/docs/admin/ru/doc-link-block/ID',

      exec: function(composer, command, value) {
        //var dropdown = this._init(composer);
        //var stream_select = dropdown.retrieve('widget');
        var widget = this._init(composer);
        if (!value){
          //dropdown.setStyle('display', dropdown.style.display == 'none'? '': 'none');
        } else if(value == 'select'){
          widget.show();
        } else {
          var aside = this.createElement(value);
          insertBlock(composer, aside);
          widget.hide();
        }
      },

      createElement: function(value){
        var aside = new Element(this.tagName, {
          'item_id': value,
          'data-align': 'center'
        });
        return this.prepareElement(aside);
      },

      prepareElement: function(aside){
        var value = aside.getAttribute('item_id');
        var win = aside.ownerDocument.defaultView;
        aside.setAttribute('contenteditable', 'false');

        if (! aside.querySelector('iframe')){
          var iframe = new Element('iframe', {'src': this.url.replace('ID', value).replace('STREAM',$('doclink_button').get('data-stream')) });
          var that = this;
          iframe.addEventListener('load', function() {
              iframe.style.width = '700px';
              var height = iframe.contentWindow.document.body.scrollHeight + 'px';
              if (win.composer) {
                  win.composer.withNoHistory(function() {
                      iframe.style.height = height;
                  });
              } else {
                  iframe.style.height = height;
              }
          }, false);
          aside.appendChild(iframe);

          aside.classList.add('replaceble-block');

          var rmBtn = new Element('button');
          rmBtn.className = 'remove';
          rmBtn.addEventListener('click', function(){
            aside.parentNode.removeChild(aside);
          });
          aside.appendChild(rmBtn);

          var upBtn = new Element('button');
          upBtn.className = 'move-up';
          upBtn.addEventListener('click', function(){
            if(aside.previousElementSibling) {
              aside.parentNode.insertBefore(aside, aside.previousElementSibling);
            }
          });
          aside.appendChild(upBtn);

          var downBtn = new Element('button');
          downBtn.className = 'move-down';
          downBtn.addEventListener('click', function(){
            if(aside.nextElementSibling) {
              aside.parentNode.insertBefore(aside, aside.nextElementSibling.nextElementSibling);
            }
          });
          aside.appendChild(downBtn);
          
          /*var rightBtn = new Element('button');
          rightBtn.className = 'move-right';
          rightBtn.addEventListener('click', function(){
            aside.dataset.align = 'right';
          });
          aside.appendChild(rightBtn);

          var centerBtn = new Element('button');
          centerBtn.className = 'move-center';
          centerBtn.addEventListener('click', function(){
            aside.dataset.align = 'center';
          });
          aside.appendChild(centerBtn);

          if (0){
            var leftBtn = new Element('button');
            leftBtn.className = 'move-left';
            leftBtn.addEventListener('click', function(){
              aside.dataset.align = 'left';
            });
            aside.appendChild(leftBtn);

          }
          */
        }
        return aside;
      }
  };

  var InlineLinkPlugin = Object.append(
    Object.create(wysihtml5.commands.PopupStreamSelectPlugin), {
      tagName: 'A',
      createElement: function(value){
        return new Element(this.tagName, {'href': 'model://'+this.propertyName + "/" + value});
      },

      elementMatches: function(el){
        var href = el.getAttribute('href');
        return href &&
               href.substr(0, 8) == 'model://' &&
               href.split('/')[2] == this.propertyName &&
               href.split('/')[3] &&
               href.split('/')[4] === undefined;
      }
    });




  wysihtml5.commands.objectLink = {
    exec: function(composer, command, value) {
      var dropdown = composer.textarea.element
                             .getParent('.wysihtml5-widget')
                             .getElement('[data-wysihtml5-dialog="ObjectLink"]');
      dropdown.setStyle('display', dropdown.style.display == 'none'? '': 'none');
    }
  }


  function replaceBlocks(element){
    for (var cmd in wysihtml5.commands) if (wysihtml5.commands.hasOwnProperty(cmd)){
      cmd = wysihtml5.commands[cmd];
      if (cmd.prepareElement){
        var tag = cmd.tagName.toLowerCase();
        var asides = element.querySelectorAll(tag); // XXX crossbrowser?
        for (var i=asides.length; i--;){
          cmd.prepareElement(asides[i]);
        }
      }
    }
  }
  window.replaceDocBlocks = replaceBlocks;


  function insertBlock(composer, block){
    // console.log('composer', composer);
    // console.log('block', block);
    var range = composer.selection.getRange().nativeRange;
    range.splitBoundaries();
    var place = range.startContainer;
    if (place.tagName == 'BODY') {
        if(place.firstChild){ 
            place = place.firstChild;
        }else{
          var p = new Element('p', {'html': '&nbsp;'});
          p.inject(place);
          place = p;
        }
    }

    while (place.parentNode.tagName != 'BODY') {
      place = place.parentNode
    }
    if (place.previousSibling) {
        block.inject(place.previousSibling, 'after');
        //place.parentNode.insertAfter(block, place.previousSibling);
    }else if (place.nextSibling){
        block.inject(place.nextSibling, 'before');
        //place.parentNode.insertBefore(block, place.nextSibling);
    }else{
       block.inject(place, 'top');
    }

    var isLast = true, last = block.nextSibling;
    while (last) { 
      if (last.textContent.trim()){ isLast = false; break; }
      last = last.nextSibling;
    }
    if (isLast && place.tagName!='P') {
      var p = new Element('p', {'html': '&nbsp;'});
      place.parentNode.insertBefore(p, block.nextSibling);
    }
  }


  var DocLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_DOCLINK',
      widgetName: 'links_blocks', 
      commandName: 'doclink',
      // XXX show front version from front widget
      url: 'STREAM/doc-link-block/ID',
      getWidget: function(formId){
          var fieldlist = $(formId + '-' + this.widgetName).retrieve('widget');
          return new PopupFieldListSelect(fieldlist);
      }
  });
  wysihtml5.commands.doclink = DocLinkPlugin;


  var FilesLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_FILES',
      widgetName: 'files_blocks', 
      commandName: 'fileslink',
      // XXX show front version from front widget
      url: 'STREAM/files-block/ID',
      getWidget: function(formId){
          var fieldlist = $(formId + '-' + this.widgetName).retrieve('widget');
          return new PopupFieldListSelect(fieldlist);
      }
  });
  wysihtml5.commands.fileslink = FilesLinkPlugin;



  var MediaLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_MEDIA',
      widgetName: 'medias',
      commandName: 'medialink',
      // XXX show front version from front widget
      url: 'STREAM/media-link-block/ID',
      getWidget: function(formId){
        var pss = $(formId + '-' + this.widgetName).retrieve('widget');
        return new StreamSelect(pss, {'hide_files': true});
      }
  });
  wysihtml5.commands.medialink = MediaLinkPlugin;

  var PhotoLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_PHOTO',
      widgetName: 'photo',
      commandName: 'photolink',
      // XXX show front version from front widget
      url: '/docs/admin/ru/photo-block/ID',
      getWidget: function(formId){
        var pss = $(formId + '-' + this.widgetName).retrieve('widget');
        return new StreamSelect(pss);
      }
  });

  wysihtml5.commands.photolink = PhotoLinkPlugin;


  var PhotoSetLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_PHOTOSET',
      widgetName: 'photo_sets',
      commandName: 'photosetlink',
      // XXX show front version from front widget
      url: '/docs/admin/ru/photo-set-block/ID',
      getWidget: function(formId){
        var pss = $(formId + '-' + this.widgetName).retrieve('widget');
        return new StreamSelect(pss);
      }
  });
  wysihtml5.commands.photosetlink = PhotoSetLinkPlugin;

  var AudioLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_AUDIO',
      widgetName: 'audio',
      commandName: 'audiolink',
      // XXX show front version from front widget
      url: '/docs/admin/ru/audio-block/ID',
      getWidget: function(formId){
        var pss = $(formId + '-' + this.widgetName).retrieve('widget');
        return new StreamSelect(pss);
      }
  });
  wysihtml5.commands.audiolink = AudioLinkPlugin;

  var VideoLinkPlugin = Object.append(
    Object.create(LinkPlugin), {
      tagName: 'IKTOMI_VIDEO',
      widgetName: 'video',
      commandName: 'videolink',
      // XXX show front version from front widget
      url: '/docs/admin/ru/video-block/ID',
      getWidget: function(formId){
        var pss = $(formId + '-' + this.widgetName).retrieve('widget');
        return new StreamSelect(pss);
      }
  });
  wysihtml5.commands.videolink = VideoLinkPlugin;

  wysihtml5.commands.personLink = Object.append(
    Object.create(InlineLinkPlugin), {
      propertyName: 'person',
      commandName:  'personLink',
      streamName:   'persons'
  });

  wysihtml5.commands.eventLink = Object.append(
     Object.create(InlineLinkPlugin), {
        propertyName: 'event',
        commandName:  'eventLink',
        streamName:   'events'
  });
  wysihtml5.commands.pageLink = Object.append(
     Object.create(InlineLinkPlugin), {
        propertyName: 'page',
        commandName:  'pageLink',
        streamName:   'pages'
  });



  // XXX hack!
  var setValue = wysihtml5.views.Composer.prototype.setValue;
  wysihtml5.views.Composer.prototype.setValue = function(){
    result = setValue.apply(this, arguments);
    this.withNoHistory(function(){
      replaceBlocks(this.element);
    });
    return result;
  };

  var _create = wysihtml5.views.Composer.prototype._create;
  wysihtml5.views.Composer.prototype._create = function(){
      result = _create.apply(this, arguments);
      this.element.ownerDocument.defaultView.composer = this;
      this.withNoHistory(function(){
      replaceBlocks(this.element);
    });
    return result;
  };


  var st = wysihtml5.commands.createLink.state;
  wysihtml5.commands.createLinkAdvanced = Object.append(
    Object.create(wysihtml5.commands.createLink), {
      state: function(composer, command) {
        return wysihtml5.commands.formatInline.state(composer, command, "A") ||
               wysihtml5.commands.formatInline.state(composer, command, "ABBR");
      }
    });
  var  tt = wysihtml5.commands.createLinkAdvanced.state;

  wysihtml5.commands.unlinkAdvanced = Object.append(
    Object.create(wysihtml5.commands.unlink), {
      createCommand: wysihtml5.commands.createLinkAdvanced
    });

    var FullscreenPlugin = {
        exec: function(composer, command, value) {
            composer.parent.textareaElement.parentNode.toggleClass('fullscreen');
        }
    };

    wysihtml5.commands.fullscreen = Object.append(
        Object.create(FullscreenPlugin), {}
    );

  console.log('commands', wysihtml5.commands);
})(wysihtml5);

(function(wysihtml5) {
  var REG_EXP     = /text-align-[0-9a-z]+/g;

  wysihtml5.commands.justifyLeft = {
    exec: function(composer, command) {
      return wysihtml5.commands.formatBlock.exec(composer, "formatBlock", null, null, REG_EXP);
    },

    state: function(composer, command) {
      return wysihtml5.commands.formatBlock.state(composer, "formatBlock", null, null, REG_EXP);
    }
  };
})(wysihtml5);

(function(wysihtml5) {
  var CLASS_NAME  = "text-align-center",
      REG_EXP     = /text-align-[0-9a-z]+/g;

  wysihtml5.commands.justifyCenter = {
    exec: function(composer, command) {
      return wysihtml5.commands.formatBlock.exec(composer, "formatBlock", null, CLASS_NAME, REG_EXP);
    },

    state: function(composer, command) {
      return wysihtml5.commands.formatBlock.state(composer, "formatBlock", null, CLASS_NAME, REG_EXP);
    }
  };
})(wysihtml5);

(function(wysihtml5) {
  var CLASS_NAME  = "text-align-right",
      REG_EXP     = /text-align-[0-9a-z]+/g;

  wysihtml5.commands.justifyRight = {
    exec: function(composer, command) {
      return wysihtml5.commands.formatBlock.exec(composer, "formatBlock", null, CLASS_NAME, REG_EXP);
    },

    state: function(composer, command) {
      return wysihtml5.commands.formatBlock.state(composer, "formatBlock", null, CLASS_NAME, REG_EXP);
    }
  };
})(wysihtml5);
