define ['jquery', 'underscore', 'js/app/home_view'], ($, _, home) ->
  describe 'League', ->
    it 'can create a League mode', ->
      #expect(true).toBe(true);
      #expect(_.first([1,2,3])).toBe(2);
      new home.League()
      expect(true).toBe(true);
