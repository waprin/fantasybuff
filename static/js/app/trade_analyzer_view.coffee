define ['jquery', 'underscore', 'backbone', 'app/views/tab_view', 'global'], ($, _, Backbone, tab_view, global) ->
  $ ->
    tabs = []
    # Start Backbone history a necessary step for bookmarkable URL's
    AppRouter = Backbone.Router.extend({
      routes: {
        "week/:id": "getWeek",
      }
    })
    app_router = new AppRouter()
    app_router.on 'route:getWeek', ->
      console.log "handling get week"
    Backbone.history.start();

    activeMatch = (child, name, week_id) ->
      child_id = child.attr('id')
      week_id = "week-#{week_id}"
      answer = child_id == week_id
      console.log "comparing #{child_id} to #{week_id} #{answer}"
      return answer
    for week in global.weeks
      tabs.push({'id': "week-#{week}", 'name': "Week #{week}", 'href': "week/#{week}"})
    $("#weekly-tab").append(new tab_view.TabView({"activeMatch": activeMatch, "prefix": "week", "use_id": true}).render(tabs).el)