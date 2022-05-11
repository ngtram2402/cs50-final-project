from cs50 import get_int, get_string
from random import randint, shuffle
from texttable import Texttable

# Install texttable by executing 'pip install texttable'

MAX = 25
strategies = ['copycat', 'cheater', 'naive', 'grudger', 'copykitten', 'skeptic', 'random']

# key: strategy, value: number of players
strategy_count = {}

# players dict, key: player0, player1...player24, value = Player(strategy, score, cheated, mistake)
players = {}

# cheated: opponents cheated self
# mistake: opponents self cheated by mistake
class Player:
    def __init__(self, strategy, score, cheated, mistake):
        self.strategy = strategy
        self.score = score
        self.cheated = cheated
        self.mistake = mistake

# Dictionary of scenarios - dictionary (p_mistake, rounds_per_match, strategy_count)
all_scenario = {}

def main():
    # Start game
    status = 'Y'
    while status == 'Y':
        # If new game: create new scenario
        if len(all_scenario) == 0:
            reuse_ans = 'N'
            # Ask for number of players for each strategies, and save to strategy_count dictionary
            save_strategies()
            # Ask for probability of mistake (0-50)
            p_mistake = ask_mistake()
            # Ask for number of rounds per match (> 0)
            rounds_per_match = ask_rounds()

            # Save inputs to all_scenario dictionary
            while True:
                ans = get_string('Save as scenario? (Y/N) ').upper()
                if ans == 'Y' or ans == 'N':
                    break
            # Save as scenario
            if ans == 'Y':
                while True:
                    scenario_name = get_string('Scenario name: ')
                    # If scenario_name != 'temp' --> end ask. If duplicate --> notify, ask again
                    if scenario_name != 'temp':
                        break
                    print('Scenario name already taken. Please choose another name.')
            else:
                # Save as temporary scenario
                scenario_name = 'temp'
            # Save inputs to all_scenario dictionary
            all_scenario[scenario_name] = {}
            scenario = all_scenario[scenario_name]
            scenario['strategy_count'] = strategy_count.copy()
            scenario['p_mistake'] = p_mistake
            scenario['rounds_per_match'] = rounds_per_match

        # If coninued game
        else:
            while True:
                reuse_ans = get_string('Reuse previous scenario? (Y/N) ').upper()
                if reuse_ans == 'Y' or reuse_ans == 'N':
                    break
            # Reuse previous scenario
            if reuse_ans == 'Y':
                # Scenario_name unchanged
                scenario = all_scenario[scenario_name]
                # Get inputs
                for strategy in strategy_count:
                    for new_strategy in scenario['strategy_count']:
                        if strategy == new_strategy:
                            strategy_count[strategy] = scenario['strategy_count'][strategy]
                rounds_per_match = scenario['rounds_per_match']
                p_mistake = scenario['p_mistake']
                
                # Print scenario details as table
                print('Previous scenario:')
                table = Texttable()
                # Table header
                header1 = ['name', 'mistake', 'rounds']
                header2 = list(scenario['strategy_count'].keys())
                table.header(header1 + header2)
                # Table row
                row1 = [scenario_name, str(scenario['p_mistake']), str(scenario['rounds_per_match'])]
                row2 = list(scenario['strategy_count'].values())
                table.add_row(row1 + row2)
                # Formatting
                table.set_cols_width([8, 7, 6, 7, 7, 7, 7, 10, 7, 7])
                table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
                # Print table
                print(table.draw())

            # Don't reuse previous scenario
            else:
                print('')
                print('Choose created scenario: C')
                print('Create new scenario and save: S')
                print('Create new scenario but do not save: N')
                print('Quit: Q')
                print('')
                choices = ['C', 'S', 'N', 'Q']

                # Print table of all created scenarios
                print('Scenarios created:')
                table = Texttable()
                # Table header
                header1 = ['name', 'mistake', 'rounds']
                table.header(header1 + strategies)
                # Table row
                for scenario_name in all_scenario:
                    scenario = all_scenario[scenario_name]
                    row1 = [scenario_name, str(scenario['p_mistake']), str(scenario['rounds_per_match'])]
                    row2 = list(scenario['strategy_count'].values())
                    table.add_row(row1 + row2)
                # Formatting
                table.set_cols_width([8, 7, 6, 7, 7, 7, 7, 10, 7, 7])
                table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c'])
                # Print table
                print(table.draw())

                # Ask choice
                while True:
                    ans = get_string('Your choice? ').upper()
                    if ans in choices:
                        break

                # Choose created scenario
                if ans == 'C':
                    # Choose scenario
                    while True:
                        scenario_name = get_string('Scenario name: ')
                        if scenario_name in all_scenario.keys():
                            break
                        print('Scenario name not available. Please recheck spelling')

                    scenario = all_scenario[scenario_name]
                    # Get new scenario's inputs
                    for strategy in strategy_count:
                        for new_strategy in scenario['strategy_count']:
                            if strategy == new_strategy:
                                strategy_count[strategy] = scenario['strategy_count'][strategy]
                    rounds_per_match = scenario['rounds_per_match']
                    p_mistake = scenario['p_mistake']

                # Create new scenario
                elif ans == 'S' or ans == 'N':
                    # Ask for number of players for each strategies, and save to strategy_count dictionary
                    save_strategies()
                    # Ask for probability of mistake (0-50)
                    p_mistake = ask_mistake()
                    # Ask for number of rounds per match (> 0)
                    rounds_per_match = ask_rounds()

                    # Create new scenario and save
                    if ans == 'S':
                        while True:
                            scenario_name = get_string('Scenario name: ')
                            # If scenario_name not duplicate --> break. If duplicate: notify, ask again
                            if scenario_name not in list(all_scenario.keys()):
                                break
                            print('Scenario name already taken. Please choose another name.')

                    # Save as temporary scenario
                    else:
                        scenario_name = 'temp'

                    # Save inputs to scenario dictionary
                    all_scenario[scenario_name] = {}
                    scenario = all_scenario[scenario_name]
                    scenario['strategy_count'] = strategy_count.copy()
                    scenario['p_mistake'] = p_mistake
                    scenario['rounds_per_match'] = rounds_per_match

                # Quit
                else:
                    quit()

        # Ask for number of matches (>0)
        matches = ask_matches()

        # Remove strategies with count = 0 from strategy_count (Unless reuse scenario)
        if reuse_ans != 'Y':
            strategy_count_copy = strategy_count.copy()
            for strategy in strategy_count_copy:
                if strategy_count_copy[strategy] == 0:
                    strategy_count.pop(strategy)
        # Reset reuse_ans
        reuse_ans = 'N'

        # players dict, key: player0, player1...player24, value = Player(strategy, score, cheated, mistake)
        player_index = 0
        for strategy in strategy_count:
            for i in range(strategy_count[strategy]):
                # Initital score = 0, empty cheated and mistake list
                players['player' + str(player_index)] = Player(strategy, 0, [], [])
                player_index = player_index + 1

        # Print table of number of players per strategy
        table = Texttable()
        # Table header
        header = ['match #'] + list(strategy_count.keys())
        table.header(header)
        # Set column width
        cols_width = []
        for i in range(len(strategy_count) + 1):
            cols_width.append(10)
        table.set_cols_width(cols_width)
        # Set alignment center
        cols_align = []
        for i in range(len(strategy_count) + 1):
            cols_align.append('c')
        table.set_cols_align(cols_align)
        # Print initial count of players
        row = ['initial'] + list(strategy_count.values())
        table.add_row(row)

        # Tournament
        for i in range(matches):
            match(rounds_per_match)
            # Update number of players per strategy
            for strategy in strategy_count:
                strategy_count[strategy] = 0
            for player in players:
                for strategy in strategy_count:
                    if players[player].strategy == strategy:
                        strategy_count[strategy] = strategy_count[strategy] + 1
            # Table row for match result
            row = ['match ' + str(i + 1)] + list(strategy_count.values())
            table.add_row(row)

        # Print table
        print(table.draw())

        # Ask if player wants to play again
        while True:
            status = get_string('Play again? (Y/N) ').upper()
            if status == 'Y' or status == 'N':
                break

    # Quit game if status = 'n'
    quit()


# Ask for number of players for each strategies, and save to strategy_count dictionary
def save_strategies():
    players_left = MAX
    for strategy in strategies:
        # If last strategy in list --> auto = players_left
        if strategies.index(strategy) == len(strategies) - 1:
            strategy_count[strategy] = players_left
            print('Number of ' + strategy + 's: ' + str(strategy_count[strategy]))
        else:
            ask_strategies(strategy, players_left)
            # If valid input (not surpass players_left) --> accept, move on to next strategy
            if strategy_count[strategy] < players_left:
                players_left = players_left - strategy_count[strategy]
            # If players_left == 0 --> Set unasked strategies = 0 (to save as scenario), then end ask
            elif strategy_count[strategy] == players_left:
                # List of unasked strategies
                unasked = strategies.copy()
                last_index = unasked.index(strategy)
                for i in range(0, last_index + 1):
                    unasked.pop(0)
                # All unasked strategies: 0
                for strategy in strategies:
                    if strategy in unasked:
                        strategy_count[strategy] = 0
                break
    return


# Ask for number of players for strategy
def ask_strategies(strategy, players_left):
    print(str(players_left) + ' players left')
    # Save number of players for strategy
    strategy_count[strategy] = get_int('Number of ' + strategy + 's: ')
    # If invalid input (surpass players_left or <0) --> ask again
    if strategy_count[strategy] > players_left or strategy_count[strategy] < 0:
        ask_strategies(strategy, players_left)


# Ask for number of rounds per match (> 0)
def ask_rounds():
    rounds_per_match = 0
    while rounds_per_match <= 0:
        rounds_per_match = get_int('Number of rounds per match: ')
    return rounds_per_match


# Ask for number of matches (>0)
def ask_matches():
    matches = 0
    while matches <= 0:
        matches = get_int('Number of matches: ')
    return matches


# Ask for probability of mistake (0-50)
def ask_mistake():
    global p_mistake
    p_mistake = -1
    while p_mistake < 0 or p_mistake > 50:
        p_mistake = get_int('Probability of mistake (%): ')
    return p_mistake

# a: 'player0'... 'player19'
# Get a's action for this round
def action(a, b):
    rand = randint(1, 100)
    # a cheat b by mistake
    if rand <= p_mistake:
        a_action = 'cheat'
        # a remembers that this turn a cheats b by mistake
        players[a].mistake.append(b)
    else:
        # This turn a doesn't cheat b by mistake
        if b in players[a].mistake:
            players[a].mistake.remove(b)
        # Copycat: cheat if opponent cheated last turn. Grudger: cheat if opponent cheated before
        if players[a].strategy == 'copycat' or players[a].strategy == 'grudger':
            if b not in players[a].cheated:
                a_action = 'co-op'
            else:
                a_action = 'cheat'
        # Cheater: always cheat
        elif players[a].strategy == 'cheater':
            a_action = 'cheat'
        # Naive: always co-op
        elif players[a].strategy == 'naive':
            a_action = 'co-op'
        # Copykitten: cheat if opponent cheated last 2 turns (twice in a row)
        elif players[a].strategy == 'copykitten':
            if players[a].cheated.count(b) < 2:
                a_action = 'co-op'
            else:
                a_action = 'cheat'
        # Skeptic: if opponent cheated once, cheat back twice
        elif players[a].strategy == 'skeptic':
            if players[a].cheated.count(b) == 0:
                a_action = 'co-op'
            else:
                a_action = 'cheat'
        # Random: 50-50
        elif players[a].strategy == 'random':
            if rand <= 50:
                a_action = 'co-op'
            else:
                a_action = 'cheat'
    return a_action


# a:co-op, b: co-op
def coop(a, b):
    players[a].score = players[a].score + 2
    players[b].score = players[b].score + 2
    # This turn b doesn't cheat a
    if players[a].strategy == 'copycat' and b in players[a].cheated:
        players[a].cheated.remove(b)
    elif players[a].strategy == 'copykitten' and players[a].cheated.count(b) == 2:
        for i in range(2):
            players[a].cheated.remove(b)
    elif players[a].strategy == 'skeptic' and players[a].cheated.count(b) > 0:
        players[a].cheated.remove(b)

    # This turn a doesn't cheat b
    if players[b].strategy == 'copycat' and a in players[b].cheated:
        players[b].cheated.remove(a)
    elif players[b].strategy == 'copykitten' and players[b].cheated.count(a) == 2:
        for i in range(2):
            players[b].cheated.remove(a)
    elif players[b].strategy == 'skeptic' and players[b].cheated.count(a) > 0:
        players[b].cheated.remove(a)


# a: cheat, b: co-op
def cheat(a, b):
    players[a].score = players[a].score + 3
    players[b].score = players[b].score - 1
    # If last turn b cheated a by mistake --> b forgive a, don't append a in cheated
    if a in players[b].mistake:
        players[b].mistake.remove(a)

    else:
        if (players[b].strategy == 'copycat' or players[b].strategy == 'grudger') and a not in players[b].cheated:
            players[b].cheated.append(a)
        elif players[b].strategy == 'copykitten' and players[b].cheated.count(a) < 2:
            players[b].cheated.append(a)
        elif players[b].strategy == 'skeptic':
            for i in range(2):
                players[b].cheated.append(a)


# a: cheat, b: cheat
def nothing(a, b):
    # If last turn a cheated b by mistake --> a forgive b, don't append b in cheated
    if b in players[a].mistake:
        players[a].mistake.remove(b)
    else:
        if (players[a].strategy == 'copycat' or players[a].strategy == 'grudger') and b not in players[a].cheated:
            players[a].cheated.append(b)
        elif players[a].strategy == 'copykitten' and players[a].cheated.count(b) < 2:
            players[a].cheated.append(b)
        elif players[a].strategy == 'skeptic':
            for i in range(2):
                players[a].cheated.append(b)

    # If last turn b cheated a by mistake --> b forgive a, dont append a in cheated
    if a in players[b].mistake:
        players[b].mistake.remove(a)
    else:
        if (players[b].strategy == 'copycat' or players[b].strategy == 'grudger') and a not in players[b].cheated:
            players[b].cheated.append(a)
        elif players[b].strategy == 'copykitten' and players[b].cheated.count(a) < 2:
            players[b].cheated.append(a)
        elif players[b].strategy == 'skeptic':
            for i in range(2):
                players[b].cheated.append(a)


# Pit a and b against each other
def duel(a, b):
    # Get a and b's actions
    a_action = action(a, b)
    b_action = action(b, a)

    if a_action == 'co-op':
        if b_action == 'co-op':
            coop(a, b)
        else:
            cheat(b, a)
    else:
        if b_action == 'co-op':
            cheat(a, b)
        else:
            nothing(a, b)


# For each round: pit each 2 players against each other
# 0-1, 0-2... 0-24, 1-2,...1-24,...23-24
def round():
    for i in range(MAX - 1):
        a = 'player' + str(i)
        for j in range(i + 1, MAX):
            b = 'player' + str(j)
            duel(a, b)


# For each match: repeat n rounds, eliminate bottom 5 players and reproduce top 5 players, then reset all scores and cheated list
def match(n):
    for i in range(n):
        round()

    # Random shuffle dict (previous: order by strategy --> biased top 5 - always copycat)
    items_list = list(players.items())
    shuffle(items_list)
    players_shuffled = dict(items_list)

    # Sort players dictionary by score (desc)
    # sorted(sequence to sort, key=Function to execute to decide the order)
    players_sorted = dict(sorted(players_shuffled.items(), key=lambda item: -item[1].score))

    # Get top5 and bottom5
    bottom = []
    top = []
    # player15 --> player4, player 16 --> player 3
    for i in range(MAX - 5, MAX):
        bottom.append(list(players_sorted)[i])
        top.append(list(players_sorted)[MAX - 1 - i])
    # Change strategy of bottom 5 to type of top 5
    for i in range(5):
        players[bottom[i]].strategy = players[top[i]].strategy

    # Reset
    for player in players:
        players[player].score = 0
        players[player].cheated = []
        players[player].mistake = []


if __name__ == "__main__":
    main()
