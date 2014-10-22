define ['jquery', 'underscore', 'backbone', 'text!js/app/templates/league_template.ejs'], ($, _, Backbone, league_template) ->
  class League extends Backbone.Model

  class EspnLeagues extends Backbone.Collection
    url: '/leagues'
    model: League
    initialize: ->
      _.bindAll @, 'fetch'

  class LeagueView extends Backbone.View

    tagName: 'li'

    template: _.template(league_template)

    initialize: ->
      @listenTo @model, 'change', @render

    render: ->
      model = @model.toJSON()
      model.percent_done = (100 * model.pages_scraped) / model.total_pages
      @$el.html(@template(model))
      @

  class AppView extends Backbone.View

    el : $("#accounts_app")

    initialize: ->
      @listenTo @collection, 'add', @addOne
      @collection.fetch()

      @collection.on 'sync', ->
        isLoaded = (model) ->
          model.get('loaded')

        if _.some @collection.models, isLoaded
          setTimeout @collection.fetch, 5000

    addOne: (league) ->
      leagueView = new LeagueView { model: league }
      $('#accounts_list').append(leagueView.render().el)
  return {
  League: League
  EspnLeagues: EspnLeagues
  LeagueView: LeagueView
  AppView: AppView
  }












