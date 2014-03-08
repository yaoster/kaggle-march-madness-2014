#!/usr/bin/env python

import csv
from itertools import izip
import numpy as np

# directories
DATA = '/Users/dyao/src/kaggle/kaggle-march-madness-2014/data/'
#DATA = '/home/yaoster/kaggle/kaggle-march-madness-2014/data/'

# input files
TEAMS = DATA + 'teams.csv'
TOURNEY_RESULTS = DATA + 'tourney_results.csv'
REG_RESULTS = DATA + 'regular_season_results.csv'
SLOTS = DATA + 'tourney_slots.csv'
SEEDS = DATA + 'tourney_seeds.csv'
SEASONS = DATA + 'seasons.csv'
RANKINGS = DATA + 'ordinal_ranks_core_33.csv'

# output files
OUTPUT_FILE = DATA + 'features.csv'
HEADER = ['target', 'gameid', 'hteam' ,'lteam', 'round', 'hseed', 'lseed', 'seed_diff', \
          'hseed_record', 'hseed_avg_ps', 'hseed_median_ps', 'hseed_std_ps', 'hseed_skew_ps', \
          'hseed_kurtosis_ps', 'lseed_record', 'lseed_avg_ps', 'lseed_median_ps', 'lseed_std_ps', \
          'lseed_skew_ps', 'lseed_kurtosis_ps', \
          'wlk_hrank_first', 'wlk_hrank_last', 'wlk_hrank_last_vs_first', 'wlk_hrank_last_vs_first_ps', \
          'wlk_lrank_first', 'wlk_lrank_last', 'wlk_lrank_last_vs_first', 'wlk_lrank_last_vs_first_ps', \
          'wlk_ps_first', 'wlk_ps_last', 'wlk_ps_last_vs_first', \
          'dol_hrank_first', 'dol_hrank_last', 'dol_hrank_last_vs_first', 'dol_hrank_last_vs_first_ps', \
          'dol_lrank_first', 'dol_lrank_last', 'dol_lrank_last_vs_first', 'dol_lrank_last_vs_first_ps', \
          'dol_ps_first', 'dol_ps_last', 'dol_ps_last_vs_first', \
          'col_hrank_first', 'col_hrank_last', 'col_hrank_last_vs_first', 'col_hrank_last_vs_first_ps', \
          'col_lrank_first', 'col_lrank_last', 'col_lrank_last_vs_first', 'col_lrank_last_vs_first_ps', \
          'col_ps_first', 'col_ps_last', 'col_ps_last_vs_first', \
          'sag_hrank_first', 'sag_hrank_last', 'sag_hrank_last_vs_first', 'sag_hrank_last_vs_first_ps', \
          'sag_lrank_first', 'sag_lrank_last', 'sag_lrank_last_vs_first', 'sag_lrank_last_vs_first_ps', \
          'sag_ps_first', 'sag_ps_last', 'sag_ps_last_vs_first']


def load_games():
    games = { } # (season, high # team, low # team) -> (wteam, wscore, lteam, lscore, slot)
    with open(TOURNEY_RESULTS, 'r') as f:
        with open(SLOTS, 'r') as fslots:
            header = True
            csvreader = csv.reader(f, delimiter=',')
            slotreader = csv.reader(fslots, delimiter=',')
            for row, slotrow in izip(csvreader, slotreader):
                if header:
                    header = False
                    continue
                (season, daynum, wteam, wscore, lteam, lscore) = \
                    (str(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]))
                games[(season, max(wteam, lteam), min(wteam, lteam))] = \
                        (wteam, wscore, lteam, lscore, slotrow[1])
    return games


def load_seeds():
    seeds = { } # season -> team # -> (region, seed)
    with open(SEEDS, 'r') as f:
        header = True
        csvreader = csv.reader(f, delimiter=',')
        for row in csvreader:
            if header:
                header = False
                continue
            (season, seed, team) = (str(row[0]), str(row[1]), int(row[2]))
            if season not in seeds:
                seeds[season] = { }
            seeds[season][team] = seed
    return seeds


def load_rankings():
    rankings = { } # season -> team # -> name -> (day, ranking)
    with open(RANKINGS, 'r') as f:
        header = True
        csvreader = csv.reader(f, delimiter=',')
        for row in csvreader:
            if header:
                header = False
                continue
            (season, day, name, team, rank) = (str(row[0]), int(row[1]), str(row[2]), int(row[3]), int(row[4]))
            if season not in rankings:
                rankings[season] = { }
            if team not in rankings[season]:
                rankings[season][team] = { }
            if name not in rankings[season][team]:
                rankings[season][team][name] = []
            if day < 134:
                rankings[season][team][name].append((day, rank))
    return rankings


def load_results(filename):
    results = { } # season -> team # -> ([(win ps, opponent)], [(loss ps, opponent)])
    with open(filename) as f:
        header = True
        csvreader = csv.reader(f, delimiter=',')
        for row in csvreader:
            if header:
                header = False
                continue
            (season, daynum, wteam, wscore, lteam, lscore, wloc) = \
                (str(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), str(row[6]))
            if season not in results:
                results[season] = { }
            if wteam not in results[season]:
                results[season][wteam] = ([], [])
            if lteam not in results[season]:
                results[season][lteam] = ([], [])
            ps = wscore - lscore
            results[season][wteam][0].append((ps, lteam))
            results[season][lteam][1].append((-1*ps, wteam))
    return results


def write_data(games, seeds, rankings, results):
    with open(OUTPUT_FILE, 'w') as f:
        csvwriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(HEADER)
        for game in games.keys():
            (season, hteam, lteam) = game
            (wteam, wscore, lteam, lscore, slot) = games[game]
            wteam_seed = int(seeds[season][wteam][1:3])
            lteam_seed = int(seeds[season][lteam][1:3])
            hsteam = 0
            lsteam = 0
            hseed = 0
            lseed = 0
            if wteam_seed <= lteam_seed:
                hsteam = wteam
                lsteam = lteam
                hseed = wteam_seed
                lseed = lteam_seed
                target = wscore - lscore
            else:
                hsteam = lteam
                lsteam = wteam
                hseed = lteam_seed
                lseed = wteam_seed
                target = lscore - wscore
            game_id = season + '_' + str(hteam) + '_' + str(lteam)
            row = [target, game_id, hsteam, lsteam, int(slot[1]), hseed, lseed, lseed - hseed]
            row = row + (regular_season_features(hsteam, season, results))
            row = row + (regular_season_features(lsteam, season, results))
            row = row + (ranking_features('WLK', hsteam, lsteam, season, rankings))
            row = row + (ranking_features('DOL', hsteam, lsteam, season, rankings))
            row = row + (ranking_features('COL', hsteam, lsteam, season, rankings))
            row = row + (ranking_features('SAG', hsteam, lsteam, season, rankings))
            csvwriter.writerow(row)


def regular_season_features(team, season, results):
    ps = results[season][team]
    wins = [x[0] for x in ps[0]]
    losses = [x[0] for x in ps[1]]
    ps = wins + losses
    ret = [float(len(wins))/len(wins + losses), np.mean(ps), np.median(ps), np.std(ps), \
           skewness(ps), kurtosis(ps)]
    return ret


def ranking_features(name, hsteam, lsteam, season, rankings):
    if season not in rankings:
        return ['NA']*11
    hrank_first = rankings[season][hsteam][name][0][1]
    hrank_last = rankings[season][hsteam][name][-1][1]
    hrank_first_ps = rank_to_rating(hrank_first)
    hrank_last_ps = rank_to_rating(hrank_last)
    lrank_first = rankings[season][lsteam][name][0][1]
    lrank_last = rankings[season][lsteam][name][-1][1]
    lrank_first_ps = rank_to_rating(lrank_first)
    lrank_last_ps = rank_to_rating(lrank_last)
    vs_first = hrank_first_ps - lrank_first_ps
    vs_last = hrank_last_ps - lrank_last_ps
    ret = [hrank_first, hrank_last, hrank_last - hrank_first, hrank_last_ps - hrank_first_ps, lrank_first, \
           lrank_last, lrank_last - lrank_first, lrank_last_ps - lrank_first_ps, vs_first, vs_last, vs_last - vs_first]
    return ret


def skewness(x):
    return 3*(np.mean(x) - np.median(x)) / np.std(x)


def kurtosis(x):
    n = float(len(x))
    xbar = np.mean(x)
    x4 = sum([float(xi - xbar)**4 for xi in x])/n
    return x4/np.var(x) - 3


def rank_to_rating(rank):
    return 100 - 4*np.log(rank + 1) - rank/22


def main():
    games = load_games()
    seeds = load_seeds()
    rankings = load_rankings()
    results = load_results(REG_RESULTS)
    write_data(games, seeds, rankings, results)

if __name__ == '__main__':
    main()
