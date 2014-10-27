define ['jquery', 'app/home_view'], ($, home) ->
  $ ->
    Leagues = new home.EspnLeagues()
    new home.AppView({collection: Leagues})


