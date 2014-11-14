define ['jquery', 'app/home_view', 'bootstrap'], ($, home) ->
  $ ->
    Leagues = new home.EspnLeagues()
    new home.AppView({collection: Leagues})

