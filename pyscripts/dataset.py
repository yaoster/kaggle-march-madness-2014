#!/usr/bin/env python

import csv
from itertools import izip
import numpy as np
import pdb

# directories
#HOME = '/Users/dyao/src/kaggle/kaggle-march-madness-2014/'
HOME = '/home/yaoster/kaggle/kaggle-march-madness-2014/'
DATA = HOME + 'data/'

# input files
TEAMS = DATA + 'teams.csv'
TOURNEY_RESULTS = DATA + 'tourney_results.csv'
REG_RESULTS = DATA + 'regular_season_results.csv'
SLOTS = DATA + 'tourney_slots.csv'
SEEDS = DATA + 'tourney_seeds.csv'
SEASONS = DATA + 'seasons.csv'

# output files
OUTPUT_FILE = DATA + 'features.csv'
HEADER = ['target', 'gameid', 'hteam' ,'lteam', 'round', 'hseed', 'lseed', 'seed_diff', \
          'hseed_record', 'hseed_avg_ps', 'hseed_median_ps', 'hseed_std_ps', 'hseed_skew_ps', \
          'hseed_kurtosis_ps', 'lseed_record', 'lseed_avg_ps', 'lseed_median_ps', 'lseed_std_ps', \
          'lseed_skew_ps', 'lseed_kurtosis_ps']

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

def write_data(games, seeds, results):
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
            csvwriter.writerow(row)

def regular_season_features(team, season, results):
    ps = results[season][team]
    wins = [x[0] for x in ps[0]]
    losses = [x[0] for x in ps[1]]
    ps = wins + losses
    ret = [float(len(wins))/len(wins + losses), np.mean(ps), np.median(ps), np.std(ps), \
           skewness(ps), kurtosis(ps)]
    return ret

def skewness(x):
    return 3*(np.mean(x) - np.median(x)) / np.std(x)

def kurtosis(x):
    n = float(len(x))
    xbar = np.mean(x)
    x4 = sum([float(xi - xbar)**4 for xi in x])/n
    return x4/np.var(x) - 3

def main():
    games = load_games()
    seeds = load_seeds()
    results = load_results(REG_RESULTS)
    write_data(games, seeds, results)

if __name__ == '__main__':
    main()
