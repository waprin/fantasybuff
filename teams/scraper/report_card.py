from django.core.cache import cache
from teams.models import TeamReportCard, TeamWeekScores, League, Team
import simplejson as json

__author__ = 'bprin'

import logging
logger = logging.getLogger(__name__)

from django.core.serializers.json import Serializer as Builtin_Serializer

class Serializer(Builtin_Serializer):
    def get_dump_object(self, obj):
        return self._current


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