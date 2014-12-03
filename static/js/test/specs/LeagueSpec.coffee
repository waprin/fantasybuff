define ['jquery', 'underscore', 'app/home_view'], ($, _, home) ->
  describe 'Queue LeagueView', ->
    it 'will show that the league is queued', ->
      league = new home.League()
      league.set
        name: 'test_league'
        year: '2014'
        pages_scraped: 20
        total_pages: 100
        loaded: false
        loading: false
        failed: false
      leagueView = new home.LeagueView({model: league})
      el = leagueView.render().el
      console.log $(el)
      expect($(el).find('.queued').length).toEqual(1)


  describe 'Loading LeagueView', ->

    el = null
    league = new home.League()

    beforeEach ->
      league.set
        name: 'test_league'
        year: '2014'
        pages_scraped: 20
        total_pages: 100
        loaded: false
        loading: true
        failed: false
        calculating: false
      leagueView = new home.LeagueView({model: league})
      el = leagueView.render().el

    it 'will show the correct loading bar', ->
      expect($(el).find(".progress").length).toEqual(1)
      expect($(el).find(".league_loading_spinner").length).toEqual(0)
      expect($(el).find('.queued').length).toEqual(0)

    it 'will show the loading bar with the correct percentage', ->
      expect($(el).find('.progress-bar')[0].style.width).toEqual("20%")


