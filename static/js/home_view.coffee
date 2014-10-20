$ ->
  class League extends Backbone.Model

  class EspnLeagues extends Backbone.Collection
    url: '/leagues'
    model: League
    initialize: ->
      _.bindAll @, 'fetch'

  Leagues = new EspnLeagues()

  class LeagueView extends Backbone.View

    tagName: 'li'

    template: _.template($('#league_template').html())

    initialize: ->
      @.listenTo @.model, 'change', @.render

    render: ->
      console.log(@.model.toJSON())
      model = @.model.toJSON()
      model.percent_done = (100 * model.pages_scraped) / model.total_pages
      @.$el.html(@.template(model))
      @

  class AppView extends Backbone.View

    el : $("#accounts_app")

    initialize: ->
      @.listenTo Leagues, 'add', @.addOne
      Leagues.fetch()

    addOne: (league) ->
      leagueView = new LeagueView { model: league }
      $('#accounts_list').append(leagueView.render().el)

  leagueView = new AppView

  Leagues.on 'sync', ->
    console.log "leagues were synced", Leagues.models
    isLoaded = (model) ->
      model.get('loaded')

    if _.some Leagues.models, isLoaded
      setTimeout Leagues.fetch, 5000
      console.log 'set timeout was set'













