__author__ = 'bprin'

import logging

logger = logging.getLogger(__name__)

from functools import partial
from decimal import Decimal


def can_fill_slot(slot, entry):
    if slot == 'FLEX':
        return entry.player.position in ('RB', 'WR', 'TE')
    return slot == entry.player.position


def get_lineup_score(entries):
    starters = filter(lambda entry: entry.slot != 'Bench', entries)
    score = reduce(lambda points, entry: points + entry.points, starters, Decimal(0))
    return score


def calculate_optimal_lineup(entries):
    slots = [entry.slot for entry in entries]
    slots = filter(lambda slot: slot != 'Bench', slots)
    try:
        i = slots.index('FLEX')
        slots.append(slots.pop(i))
    except ValueError:
        pass

    def get_available_player(entries, optimal_entries):
        return filter(lambda entry: entry.player.espn_id not in [e.player.espn_id for e in optimal_entries], entries)

    optimal_entries = []
    for slot in slots:
        available_players = get_available_player(entries, optimal_entries)
        available_players = filter(partial(can_fill_slot, slot), available_players)

        if available_players:
            best_player = max(available_players, key=lambda entry: entry.points)
            if best_player.slot == 'Bench':
                best_player.added = True
            best_player = best_player.clone()
            best_player.slot = slot
            optimal_entries.append(best_player)

    available_players = get_available_player(entries, optimal_entries)
    for player in available_players:
        bench_player = player.clone()
        if player.slot != 'Bench':
            logger.debug("setting %s as moved to bench" % player.player.name)
            bench_player.added = False

        bench_player.slot = 'Bench'
        optimal_entries.append(bench_player)

    return optimal_entries





