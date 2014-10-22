define ['jquery', 'underscore', 'js/app/home_view'], ($, _, home) ->
  describe 'LeagueView', ->
    it 'will show the correct loading bar', ->
      league = new home.League()
      league.set
        name: 'test_league'
        year: '2014'
        pages_scraped: 50
        total_pages: 100
        loaded: false
      leagueView = new home.LeagueView({model: league})

      el = leagueView.render().el
      expect($(el).find(".progress").length).toEqual(1)
      expect($(el).find(".league_loading_spinner").length).toEqual(0)





