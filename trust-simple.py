from cs50 import get_int
from random import randint, shuffle

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


def main():
    # Ask for number of players for each strategies
    players_left = MAX
    for strategy in strategies:
        # If last strategy in list --> auto = players_left
        if strategies.index(strategy) == len(strategies) - 1:
            strategy_count[strategy] = players_left
            print('Number of ' + strategy + 's: ' + str(strategy_count[strategy]))
        else:
            ask(strategy, players_left)
            # If valid input (not surpass players_left) --> accept, move on to next strategy
            if strategy_count[strategy] < players_left:
                players_left = players_left - strategy_count[strategy]
            # If players_left == 0 --> end ask
            elif strategy_count[strategy] == players_left:
                break

    # Ask for probability of mistake (0-50)
    global p_mistake
    p_mistake = -1
    while p_mistake < 0 or p_mistake > 50:
        p_mistake = get_int('Probability of mistake (%): ')
    # Ask for number of rounds per match (> 0)
    rounds_per_match = 0
    while rounds_per_match <= 0:
        rounds_per_match = get_int('Number of rounds per match: ')
    # Ask for number of matches (>0)
    matches = 0
    while matches <= 0:
        matches = get_int('Number of matches: ')

    # players dict, key: player0, player1...player24, value = Player(strategy, score, cheated, mistake)
    player_index = 0
    for strategy in strategy_count:
        for i in range(strategy_count[strategy]):
            # Initital score = 0, empty cheated and mistake list
            players['player' + str(player_index)] = Player(strategy, 0, [], [])
            player_index = player_index + 1

    # Tournament
    for i in range(matches):
        print('Match ' + str(i + 1), end=' - ')
        match(rounds_per_match)
        # Update number of players per strategy
        for strategy in strategy_count:
            strategy_count[strategy] = 0
        for player in players:
            for strategy in strategy_count:
                if players[player].strategy == strategy:
                    strategy_count[strategy] = strategy_count[strategy] + 1
        # Print number of players per strategy
        for strategy in strategy_count:
            print(strategy + ': ' + str(strategy_count[strategy]), end=' | ')
        print("")


# Ask for number of players for strategy
def ask(strategy, players_left):
    print(str(players_left) + ' players left')
    strategy_count[strategy] = get_int('Number of ' + strategy + 's: ')
    # If invalid input (surpass players_left or <0) --> ask again
    if strategy_count[strategy] > players_left or strategy_count[strategy] < 0:
        ask(strategy, players_left)


# a: 'player0'... 'player19'
# Get a's action for this round
def action(a, b):
    rand = randint(1, 100)
    # a cheat b by mistake
    if rand <= p_mistake:
        a_action = 'cheat'
        # a remembers that this turn a cheat b by mistake
        players[a].mistake.append(b)
    else:
        # This turn a dont cheat b by mistake
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
            rand = randint(1, 100)
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


# a: cheat, b: cheat
def nothing(a, b):
    # If last turn a cheated b by mistake --> a forgive b, dont append b in cheated
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
