define ['jquery', 'underscore', 'backbone'], ($, _, Backbone) ->
  class TabView extends Backbone.View
    'tagName': 'ul',
    'className': 'nav nav-tabs'

    initialize: (options) ->
      Backbone.history.on 'route', (router, name, id) =>
        console.log("comparign to router #{router} name #{name} id #{id}")
        _.each @$el.children(), (child) ->
            console.log "in child"
            child = $(child);
            if child.attr('class') == 'dropdown'
                return;
            if options.activeMatch child, name, id[0]
                child.addClass('active')
            else
                child.removeClass('active')
        $(".week-tab").hide()
        week_id = "#week-#{id[0]}-tab"
        $(week_id).show();

    render: (tabs) ->
      first = false
      render_tab = (tab) ->
        "<li id=\"#{tab.id}\"><a href=\"##{tab.href}\">#{tab.name}</a></li> "
      @$el.append render_tab(tab) for tab in tabs
      $("#" + @$('li')[0]['id'] + "-tab").show()
      @

    ###
    if name.substring(0, 4) != 'load'
            return
        name = name.substring(5);


            if (child.attr('id').split('-')[0] == name)

    ###


  TabView: TabView