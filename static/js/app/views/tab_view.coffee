define ['jquery', 'underscore', 'backbone'], ($, _, Backbone) ->
  class TabView extends Backbone.View
    'tagName': 'ul',
    'className': 'nav nav-tabs'

    update: (name, id) ->
      if name == "getTeam"
        return
      _.each @$el.children(), (child) =>
        child = $(child)
        if child.attr('class') == 'dropdown'
          return;
        if @options.activeMatch child, name, id
          if child.hasClass('active')
            return
          $(".#{@options.prefix}-tab").hide()
          child.addClass('active')
          if @options.use_id
            week_id = "##{@options.prefix}-#{id}-tab"
          else
            week_id = "##{@options.prefix}-#{name}-tab"
          $(week_id).show();
        else
          child.removeClass('active')

    initialize: (options) ->
      @options = options
      Backbone.history.on 'route', (router, name, id) =>
        @update(name, id[0])

    render: (tabs) ->
      render_tab = (tab) ->
        "<li id=\"#{tab.id}\"><a href=\"##{tab.href}\">#{tab.name}</a></li> "
      @$el.append render_tab(tab) for tab in tabs
      $(@$('li')[0]).addClass('active')
      $("#" + @$('li')[0]['id'] + "-tab").show()
      @

  TabView: TabView