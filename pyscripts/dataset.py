#!/usr/bin/env python

import csv
from itertools import izip
import pdb

# directories
HOME = '/Users/dyao/src/kaggle/kaggle-march-madness-2014/'
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
HEADER = ['target', 'gameid', 'hteam' ,'lteam', 'seed_diff']

# output csv has:
# target: hseed - lseed point spread
# game ID - season + high team number + low team number
# hseed team number
# lseed team number
# tourney round number
# hseed
# lseed
# hseed - lseed (tweak for equal seeds)
# hseed record
# lseed record
# hseed avg point spread
# hseed median point spread
# hseed point spread SD
# hseed point spread skew
# hseed point spread kurtosis
# lseed avg point spread
# lseed median point spread
# lseed point spread SD
# lseed point spread skew
# lseed point spread kurtosis

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
                games[(season, max(wteam, lteam), min(wteam, lteam))] = (wteam, wscore, lteam, lscore, slotrow[1])
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
            (wteam, wscore, lteam, lscore, slot) = games[game]
            wteam_seed = int(seeds[game[0]][wteam][1:3])
            lteam_seed = int(seeds[game[0]][lteam][1:3])
            hsteam = 0
            lsteam = 0
            if wteam_seed <= lteam_seed:
                hsteam = wteam
                target = wscore - lscore
            else:
                lsteam = lteam
                target = lscore - wscore
            game_id = game[0] + '_' + str(game[1]) + '_' + str(game[2])
            row = [target, game_id, hsteam, lsteam, abs(wteam_seed - lteam_seed)]
            csvwriter.writerow(row)

def main():
    games = load_games()
    seeds = load_seeds()
    results = load_results(REG_RESULTS)
    write_data(games, seeds, results)

if __name__ == '__main__':
    main()
