#!/usr/bin/env python

import csv
from itertools import izip
import numpy as np
from collections import defaultdict
from os.path import expanduser

# directories
HOME= expanduser("~")
DATA = HOME + '/src/kaggle/kaggle-march-madness-2014/data/'

# input files
TOURNEY_RESULTS = DATA + 'tourney_results.csv'
PREDICTIONS = DATA + 'test_predictions.csv'
TEST_SEASON = 'Q'


def load_predictions():
    predictions = { } # game id -> probability of win
    with open(PREDICTIONS, 'r') as f:
        header = True
        csvreader = csv.reader(f, delimiter=',')
        for row in csvreader:
            if header:
                header = False
                continue
            predictions[str(row[0])] = float(row[1])
    return predictions


def load_games(predictions):
    games = [] # (game_id, pred, result)
    with open('tmp.csv', 'w') as f_out:
        csvwriter = csv.writer(f_out, delimiter=',')
        with open(TOURNEY_RESULTS, 'r') as f:
            header = True
            csvreader = csv.reader(f, delimiter=',')
            for row in csvreader:
                if header:
                    header = False
                    continue
                (season, daynum, wteam, wscore, lteam, lscore) = \
                    (str(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]))
                if season != TEST_SEASON:
                    continue
                
                game_id = ''
                result = 1
                if wteam < lteam:
                    game_id = TEST_SEASON + '_' + str(wteam) + '_' + str(lteam)
                else:
                    game_id = TEST_SEASON + '_' + str(lteam) + '_' + str(wteam)
                    result = 0
                games.append((game_id, predictions[game_id], result))
                csvwriter.writerow([game_id, predictions[game_id], result])
    return games


def logloss(games):
    loss = 0
    for game in games:
        pred = game[1]
        loss = loss + game[2]*np.log(pred) + (1 - game[2])*np.log(1 - pred)
    return (-1.0/len(games)) * loss


def main():
    predictions = load_predictions()
    games = load_games(predictions)
    print logloss(games)


if __name__ == '__main__':
    main()
