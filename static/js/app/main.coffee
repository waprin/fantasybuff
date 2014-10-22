define ['jquery', 'js/app/home_view'], ($, home) ->
  $ ->
    Leagues = new home.EspnLeagues()
    new home.AppView({collection: Leagues})


