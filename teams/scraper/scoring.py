from decimal import Decimal

__author__ = 'bprin'

from teams.models import ScoringSystem, PlayerScoreStats


def calculate_player_score(scoring_system, player):
    scoring_system = ScoringSystem()
    player = PlayerScoreStats()
    score = Decimal(0)
    score += scoring_system.py25 * (int(player.pass_yards) / 25)
    score += scoring_system.td_pass * player.pass_td
    score += scoring_system.int_thrown * player.interceptions
    # score += scoring_system.twopt_pass *


scoring_system = ScoringSystem()
scoring_system.py25 = Decimal(1)
scoring_system.td_pass = Decimal(4)
scoring_system.int_thrown = (-2)

scoring_system.run10 = Decimal(1)
scoring_system.td_run = Decimal(6)
scoring_system.twopt_rush = Decimal(2)

scoring_system.rec10 = Decimal(1)
scoring_system.rec_td = Decimal(6)
scoring_system.twopt_rush = Decimal(2)

scoring_system.kr_td = Decimal(6)
scoring_system.pr_td = Decimal(6)
scoring_system.fum_lost = Decimal(-2)
scoring_system.fum_rec_td = Decimal(6)
scoring_system.fum_ret_td = Decimal(6)

scoring_system.pat_made = Decimal(1)
scoring_system.fg_missed = Decimal(-1)
scoring_system.fg_0 = Decimal(3)
scoring_system.fg_40 = Decimal(4)
scoring_system.fg_50 = Decimal(5)

scoring_system.d_sack = Decimal(1)
scoring_system.d_int_td = Decimal(6)
scoring_system.d_fr_td = Decimal(6)
scoring_system.d_pr_td = Decimal(6)
scoring_system.d_blocked_kick = Decimal(2)
scoring_system.d_fr = Decimal(2)
scoring_system.d_kickoff_td = Decimal(6)
scoring_system.d_blocked_td = Decimal(6)
scoring_system.d_int = Decimal(2)
scoring_system.d_sf = Decimal(2)

scoring_system.d_pa_0 = Decimal(5)
scoring_system.d_pa_1 = Decimal(4)
scoring_system.d_pa_7 = Decimal(3)
scoring_system.d_pa_14 = Decimal(1)
scoring_system.d_pa_28 = Decimal(-1)
scoring_system.d_pa_35 = Decimal(-3)
scoring_system.d_pa_46 = Decimal(-5)

scoring_system.da_ya_100 = Decimal(5)
scoring_system.da_ya_199 = Decimal(3)
scoring_system.da_ya_299 = Decimal(2)
scoring_system.da_ya_399 = Decimal(-1)
scoring_system.da_ya_449 = Decimal(-3)
scoring_system.da_499 = Decimal(-5)
scoring_system.da_549 = Decimal(-6)
scoring_system.da_550 = Decimal(-7)







