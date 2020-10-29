import numpy as np
import random
import pandas as pd
import math


class GR2():
    def __init__(self, num_trials, games_per_trial, win_prob, start_amount, bet_percent):

        self.num_trials = num_trials
        self.games_per_trial = games_per_trial
        self.win_prob = win_prob
        self.start_amount = start_amount
        self.bet_percent = bet_percent

    def kelly(self, p):
        return p-(1-p)

    def simulate(self):

        outcomes = np.zeros((self.games_per_trial, self.num_trials))
        outcomes[0] = self.start_amount

        for i in range(self.num_trials):
            for j in range(1, self.games_per_trial):
                res = np.random.binomial(1, self.win_prob)

                if res > 0:
                    outcomes[j, i] = (1+self.bet_percent) * outcomes[j-1, i]
                else:
                    outcomes[j, i] = (1-self.bet_percent) * outcomes[j-1, i]
        return outcomes

    def simulate_quick(self):
        result = []
        for _ in range(self.num_trials):
            this_trial = []
            money = self.start_amount
            for _ in range(self.games_per_trial):
                if self.win_prob >= random.uniform(0, 1):
                    money += money * self.bet_percent
                else:
                    money -= money * self.bet_percent
                this_trial.append(money)
            result.append(this_trial)

        #result.sort(key=lambda x: x[-1], reverse=True)
        return result

    def num_wins(self, result):
        wins = sum([1 for i in result if i > self.start_amount])
        return wins

    def num_wins_above_target(self, result, target):

        wins_above_target = sum([1 for i in result if i > target])
        return wins_above_target

    def mean_result(self, result):
        return np.mean(result).round(2)

    def median_result(self, result):
        if np.median(result) == np.NaN:
            return 0
        else:
            return np.median(result).round(2)

    def min_max_result(self, result):
        return min(result), max(result)

    def median_per_round(self, result):
        #mpr = {i+1: np.median(result[i]).round(2) for i in range(len(result))}
        # return pd.DataFrame(list(mpr.items()), columns=['Round', 'Median Winnings'])
        return {i+1: np.log(np.median(result[i]).round(2)) for i in range(len(result))}

    def quick_median_per_round(self, result):
        #mpr = {i+1: np.median(result[i]).round(2) for i in range(len(result))}
        # return pd.DataFrame(list(mpr.items()), columns=['Round', 'Median Winnings'])
        #rounds = [[i[j] for i in result] for j in range(len(result[0]))]
        return {i+1: np.log(np.median(result[i]).round(2)) for i in range(len(result))}

    def lower_quartile(self, result):
        return {i+1: np.log(np.percentile(result[i], 25).round(2)) for i in range(len(result))}

    def quick_lower_quartile(self, result):
        return {i+1: np.log(np.percentile(result[i], 25).round(2)) for i in range(len(result))}

    def upper_quartile(self, result):
        return {i+1: np.log(np.percentile(result[i], 75).round(2)) for i in range(len(result))}

    def quick_upper_quartile(self, result):
        return {i+1: np.log(np.percentile(result[i], 75).round(2)) for i in range(len(result))}

    def get_winnings_for_each_trial(self, result):
        return pd.DataFrame(result)

    def max_result_formatted(self, result):

        results = sorted(result)[-3:]
        output = []
        while results:
            n = results.pop()
            #n = max(result)
            output.append(self.format_price(n))
        return output

    def percent_lost(self, result):

        lost = sum([1 for i in result if i < self.start_amount])
        return lost

    def format_price(self, n):
        if n > 1e6:
            millnames = ['', ' Thousand',
                         ' Million', ' Billion', ' Trillion']
            n = float(n)
            millidx = max(0, min(len(millnames)-1,
                                 int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

            return('{:.0f}{}'.format(
                n / 10**(3 * millidx), millnames[millidx]))
        else:
            if n < 100:
                n = round(n, 2)
            else:
                if n:
                    n = int(round(n, 0))
            return "{:,}".format(n)
