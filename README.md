# THE GAME OF TRUST
## Video Demo:  <https://youtu.be/0wPwHSfOfas>
## Description

A remake of [The Evolution of Trust](https://ncase.me/trust/)'s sandbox by Nicky Case, with some modifications.

Other common strategies can be found [here](http://www.prisoners-dilemma.com/common-strategy/).


## Gameplay

Each round, 2 players are paired with each other, and each has 2 choice: CO-OP (put in coin), or CHEAT (don't put in coin). If one player puts in 1 coin, the other player gets 3 coins.

There are 3 scenarios:
- If both player choose to CO-OP, each gets 2 coins.
- If one player CO-OPs, and the other player CHEATs, the former loses 1 coin, while the latter gets 3 coins
- If both player choose to CHEAT, neither gains or loses

In the tournament, for each match, each 2 players will be paired with each other, and play some number of rounds.

In each round of a match, there is a possibility that a player makes a mistake, and CHEATs while it intended to CO-OP.

I have modified the game a bit, so that if a player CHEATs by mistake and its opponent CHEATs back the next turn, it will forgive the opponent. The effects to each type's action are as follow:
- Copycat: won't CHEAT back next turn
- Grudger: won't hold a grudge, still CO-OPs next turn
- Copykitten, Skeptic: won't consider it CHEATing
- Cheater, Naive, Random: No effect
This modification tends to help Copycats, Grudgers and Skeptics survive a bit longer.


##  Strategies

- **Copycat** aka Tit-for-Tat: Starts with CO-OP, then copies opponent's last move - CHEATs back if opponent CHEATed last turn, and CO-OPs back if opponent CO-OPed last turn
- **Cheater**: Always CHEATs
- **Naive**: Always CO-OPs
- **Grudger**: CO-OPs until opponent CHEATs. After that, it always CHEATs
- **Copykitten** aka Tit-for-Two-Tats: Acts like Copycat, except that it only CHEATs if opponent CHEATed twice in a row
- **Skeptic** aka Two-Tits-for-Tat: Acts like Copycat, except that it CHEATs twice if opponent CHEATed
- **Random**: CHEATs or CO-OPs randomly with a 50/50 chance

In the orginal game, there is also:
- **Simpleton** aka Win-Stay-Lose-Shift:
    - Repeats its last move if its opponent CO-OPs (believing that since it received coin, it must have done the right thing last turn, even if it was unintentional)
    - Swiches its move if its opponent CHEATs (believing that since it didn't receive coin, it must have done the wrong thing)
- **Detective**:
    - Starts first 4 turns with CO-OP, CHEAT, CO-OP, CO-OP
    - If its opponent CHEATS at least once, after that, it will play like Copycat
    - If it opponent never CHEATs back, it will play like Cheater

However, since I believe that these 2 strategies are not common in real life, I decided not to include them in my version.


## How to use

### Simple version:
Play only 1 game. After the game ends, user has to execute the program and enter inputs again
1. Execute *python trust-simple.py* to open the program
~~~
python trust-simple.py
~~~
2. Enter the number of players for each strategies.
    - You don't have to use all 6 strategies
    - There must be **25** players in total, no more, no less
    - The program will automatically fill in the number of players for the last strategy (if there's still room)
    - The program will stop asking for the number of players if you have reached 25 players in total
3. Enter the number of rounds per match
4. Enter the number of matches
5. Enter the probability of making mistake (e.g: 5% --> enter **5**, not 0.05 or 5%)
6. Voilà! The program prints out the number of players left after each match for each strategies

### Full version:

Can play multiple games and reuse created inputs
- Install texttable library if you haven't by executing *pip install texttable*
~~~
pip install texttable
~~~
- Execute *python trust.py* to open the program
~~~
python trust.py
~~~
- Enter the number of players for each strategies, the probability of making mistake, and the number of rounds per match
- Enter *Y* or *N* to choose whether to save as a scenario
    - If *Y* is entered: Enter scenario name to save
    - If *N* is entered: Continue
- Enter the number of matches
- The program prints out the number of players left after each match for each strategies
- Enter *Y* or *N* to choose whether to play again
    - If *N* is entered: Quit the program
    - If *Y* is entered: Play again
- Enter *Y* or *N* to choose whether to reuse the previous scenario
    - If *Y* is entered: Use previous inputs, except for Number of matches
    - If *N* is entered:
        - Enter *C* to choose among the created scenario
        - Enter *S* to create a new scenario and save that scenario
        - Enter *N* to create a new scenario and but do not save that scenario
        - Enter *Q* to quit the program
