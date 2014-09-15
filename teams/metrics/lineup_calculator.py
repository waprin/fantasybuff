__author__ = 'bprin'

from functools import partial
from decimal import Decimal

def can_fill_slot(slot, entry):
    if slot == 'FLEX':
        return entry.player.position in ('RB', 'WR', 'TE')
    return slot == entry.player.position

def get_lineup_score(entries):
    print "entries is " + str(entries)
    starters = filter(lambda entry: entry.slot != 'Bench', entries)
    print "starters is " + str(starters)
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
#        print "available players: " + str(available_players) + " slot " + str(slot)

        if available_players:
            best_player = max(available_players, key=lambda entry: entry.points)
            best_player = best_player.clone()
            best_player.slot = slot
            optimal_entries.append(best_player)

    available_players = get_available_player(entries, optimal_entries)
    for player in available_players:
        bench_player = player.clone()
        bench_player.slot = 'Bench'
        optimal_entries.append(bench_player)

    return optimal_entries





