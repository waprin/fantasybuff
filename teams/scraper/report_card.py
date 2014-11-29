from django.core.cache import cache
from teams.models import TeamReportCard, TeamWeekScores, League, Team, TradeEntry
import simplejson as json

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from django.core.serializers.json import Serializer as Builtin_Serializer

class Serializer(Builtin_Serializer):
    def get_dump_object(self, obj):
        return self._current

def league_summary_cache_key(league_id, year):
    return 'ffbuff_summary_%s_%s' % (league_id, year)

def league_report_cache_key(league_id, year, team_id):
    return 'ffbuff_report_%s_%s_%s' % (league_id, year, team_id)


def get_team_report_card_json(league_id, year, team_id):

    cache_key =  league_report_cache_key(league_id, year, team_id)
    hit = cache.get(cache_key)
    if hit:
        logger.info("returning cache hit")
        return hit

    league = League.objects.get(espn_id=league_id, year=year)
    team = Team.objects.get(league=league, espn_id=team_id)
    report_cards = TeamReportCard.objects.filter(team=team)
    week_scores = TeamWeekScores.objects.filter(team=team)

    draft_scores = []
    waiver_scores = []
    trade_scores = []
    lineup_scores = []

    for week_score in week_scores:
        lineup_scores.append({'week': week_score.week, 'value': float(week_score.lineup_score)})
        draft_scores.append({'week': week_score.week, 'value': float(week_score.draft_score)})
        waiver_scores.append({'week': week_score.week, 'value': float(week_score.waiver_score)})
        trade_scores.append({'week': week_score.week, 'value': float(week_score.trade_score)})

    report_data = Serializer().serialize(report_cards, fields=('average_lineup_score', 'average_draft_score', 'average_waiver_score', 'average_trade_score'))

    #scorecard_data = Serializer().serialize(scorecards, fields=('week', 'delta'))

    #draft_data = Serializer().serialize(draft_scores, fields=('draft_score', 'week', 'waiver_score', 'trade_score'))

    reportcard_struct = json.loads(report_data)
    #scorecard_struct = json.loads(scorecard_data)
#    draft_struct = json.loads(draft_data)

    #reportcard_struct[0]['lineups'] = scorecard_struct
    reportcard_struct[0]['team_id'] = team.espn_id
    reportcard_struct[0]['lineup_scores'] = lineup_scores
    reportcard_struct[0]['draft_scores'] = draft_scores
    reportcard_struct[0]['waiver_scores'] = waiver_scores
    reportcard_struct[0]['trade_scores'] = trade_scores
    reportcard_struct[0]['lineup_max'] = TeamWeekScores.get_max(league, 'lineup_score')
    reportcard_struct[0]['lineup_min'] = TeamWeekScores.get_min(league, 'lineup_score')
    reportcard_struct[0]['trade_max'] = TeamWeekScores.get_max(league, 'trade_score')
    reportcard_struct[0]['trade_min'] = TeamWeekScores.get_min(league, 'trade_score')
    reportcard_struct[0]['waiver_max'] = TeamWeekScores.get_max(league, 'waiver_score')
    reportcard_struct[0]['waiver_min'] = TeamWeekScores.get_min(league, 'waiver_score')
    reportcard_struct[0]['draft_max'] = TeamWeekScores.get_max(league, 'draft_score')
    reportcard_struct[0]['draft_min'] = TeamWeekScores.get_min(league, 'draft_score')
    reportcard_struct[0]['num_teams'] = Team.objects.filter(league=league).count()

#    reportcard_struct[0]['max_average_lineup'] = str(TeamReportCard.get_max(league, 'average_lineup_score'))
#    reportcard_struct[0]['min_average_lineup'] = str(TeamReportCard.get_min(league, 'average_lineup_score'))

    #reportcard_struct[0]['max_average_lineup'] = '100.0'
    #reportcard_struct[0]['min_average_lineup'] = '0.0'
    #reportcard_struct[0]['average_lineup_score'] = 10

    reportcard_struct[0]['max_average_draft'] = TeamReportCard.get_max(league, 'average_draft_score')
    reportcard_struct[0]['min_average_draft'] = TeamReportCard.get_min(league, 'average_draft_score')

    reportcard_struct[0]['max_average_waiver'] = TeamReportCard.get_max(league, 'average_waiver_score')
    reportcard_struct[0]['min_average_waiver'] = TeamReportCard.get_min(league, 'average_waiver_score')

    reportcard_struct[0]['max_average_trade'] = TeamReportCard.get_max(league, 'average_trade_score')
    reportcard_struct[0]['min_average_trade'] = TeamReportCard.get_min(league, 'average_trade_score')

    reportcard_struct[0]['max_average_lineup'] = TeamReportCard.get_max(league, 'average_lineup_score')
    reportcard_struct[0]['min_average_lineup'] = TeamReportCard.get_min(league, 'average_lineup_score')

    data = json.dumps(reportcard_struct[0], use_decimal=True)
    logger.info("filling cache")
    cache.set(cache_key, data)
    return data

def get_league_request_context(league):
    hit = cache.get(league_summary_cache_key(league.espn_id, league.year))
    """
    if hit:
        logger.debug("returning cache hit for league summary")
        return hit
    """

    teams = Team.objects.filter(league=league)
    no_trade = True
    best_trade = None
    trade_left = None
    trade_right = None

    trades = TradeEntry.objects.filter(team=teams)
    logger.debug("got trades %s" % str(trades))
    sorted_trades = list(trades)
    if len(sorted_trades) > 0:
        no_trade = False
        sorted_trades.sort(key=lambda t: t.get_value_cumulative(league))
        best_trade = sorted_trades[-1]

        if best_trade.get_total_points_for(league) > best_trade.get_total_points_against(league):
            logger.debug("setting left trade as winner")
            trade_left = 'trade-winner'
            trade_right = 'trade-loser'
        else:
            logger.debug("setting left trade as loser")
            trade_left = 'trade-loser'
            trade_right = 'trade-winner'
    logger.debug("best trade is for team %s %s" % (best_trade.team.team_name, best_trade.players_added.all()))


    best_waiver = league.get_most_waiver_points()
    most_perfect_lineups = league.get_most_perfect_lineups()


    points_for = None
    points_against = None
    if best_trade:
        logger.debug("best trade added %s removed %s" % (str(best_trade.players_added.all()), str(best_trade.players_removed.all())))
        points_for = best_trade.get_total_points_for(league)
        points_against = best_trade.get_total_points_against(league)


    my_context = {
        'navigation': ['Leagues'],
        'teams': teams,
        'league': league,
        'no_trade': no_trade,
        'trade': best_trade,
        'total_points_for': points_for,
        'total_points_against': points_against,
        'left': trade_left,
        'right': trade_right,
        'best_waiver': best_waiver,
        'most_perfect_lineups': most_perfect_lineups
    }
    cache.set(league_summary_cache_key(league.espn_id, league.year), my_context)
    return my_context