from functools import partial
from django.contrib.auth.models import User

__author__ = 'bprin'

from django.utils import unittest

from teams.models import League, Team, Scorecard, ScorecardEntry, Player, EspnUser
from lineup_calculator import  calculate_optimal_lineup, get_lineup_score, can_fill_slot
from teams.utils.db_utils import clearDb

class LineupCalculatorTest(unittest.TestCase):

    def setUp(self):
        clearDb()
        user = User.objects.create_user('waprin@gmail.com', 'waprin@gmail.com')
        espn_user = EspnUser.objects.create(user=user, username='gothamcityrogues', password='sincere1')
        league = League.objects.create(name="test league", espn_id='12345', year=2013)
        rogues_team = Team.objects.create(league=league, espn_user=espn_user, espn_id='3', team_name='Gotham City Rogues', owner_name='Bill Prin')
        self.scorecard = Scorecard.objects.create(team=rogues_team, week=1, actual=True)

    def test_can_fill_slot(self):
        qb_player = Player.objects.create(name='a', position='QB', espn_id='1')
        rb_player1 = Player.objects.create(name='b', position='RB', espn_id='2')
        wr_player1 = Player.objects.create(name='f', position='WR', espn_id='6')

        qb_entry = ScorecardEntry.objects.create(scorecard=self.scorecard, player=qb_player, slot='QB', points=5.0)
        rb_entry = ScorecardEntry.objects.create(scorecard=self.scorecard, player=rb_player1, slot='Flex', points=0.0)
        wr_entry = ScorecardEntry.objects.create(scorecard=self.scorecard, player=wr_player1, slot='RB', points=5.0)

        entries = [qb_entry, rb_entry, wr_entry]
        flex_slot = partial(can_fill_slot, 'FLEX')
        self.assertTrue(flex_slot(rb_entry))
        available_players = filter(partial(can_fill_slot, 'FLEX'), entries)
        self.assertEquals(len(available_players), 2)

    def test_calculate_lineup(self):
        qb_player = Player.objects.create(name='a', position='QB', espn_id='1')
        rb_player1 = Player.objects.create(name='b', position='RB', espn_id='2')
        rb_player2 = Player.objects.create(name='c', position='RB', espn_id='3')
        rb_player3 = Player.objects.create(name='d', position='RB', espn_id='4')
        rb_player4 = Player.objects.create(name='e', position='RB', espn_id='5')

        wr_player1 = Player.objects.create(name='f', position='WR', espn_id='6')
        wr_player2 = Player.objects.create(name='g', position='WR', espn_id='7')
        wr_player3 = Player.objects.create(name='h', position='WR', espn_id='8')

        entries = []
        qb_entry = ScorecardEntry.objects.create(scorecard=self.scorecard, player=qb_player, slot='QB', points=5)
        entries.append(qb_entry)
        flex_entry = ScorecardEntry.objects.create(scorecard=self.scorecard, player=rb_player1, slot='FLEX', points=0)
        entries.append(flex_entry)
        rb_entry1 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=rb_player2, slot='RB', points=2)
        entries.append(rb_entry1)
        rb_entry2 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=rb_player3, slot='RB', points=5)
        entries.append(rb_entry2)
        wr_entry1 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=wr_player1, slot='WR', points=2)
        entries.append(wr_entry1)
        wr_entry2 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=wr_player2, slot='WR', points=9)
        entries.append(wr_entry2)
        bench_entry1 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=rb_player4, slot='Bench', points=10)
        entries.append(bench_entry1)
        bench_entry2 = ScorecardEntry.objects.create(scorecard=self.scorecard, player=wr_player3, slot='Bench', points=7)
        entries.append(bench_entry2)

        self.assertEquals(int(get_lineup_score(entries)), 5 + 2 + 5 + 2 + 9)
        optimal_lineup=calculate_optimal_lineup(entries)
        self.assertEquals(len(optimal_lineup), len(entries))
        found1 = False
        found2 = False
        for entry in optimal_lineup:
            if entry.player == rb_player1:
                self.assertIsNotNone(entry.added)
                self.assertFalse(entry.added)
                found1 = True
            if entry.player == rb_player4:
                self.assertIsNotNone(entry.added)
                self.assertTrue(entry.added)
                found2 = True
        self.assertTrue(found1 and found2)

        self.assertEquals(int(get_lineup_score(optimal_lineup)), 5 + 2 + 5 + 10 + 9 + 7)

