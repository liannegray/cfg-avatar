"""Import libraries for Avatar Top Trumps"""
import random
import time
import csv
import requests
import inflect  # terminal command: pip install inflect
import pandas as pd
from rich.console import Console  # terminal command: pip install inflect

# Global variables for draw pile needed / text formatting
draw_cards = []
console = Console()


def get_colour(text):
    """Function to format the stats to make them easier to see in the console"""
    colours = {"power": "red", "defence": "blue", "agility": "magenta",
               "wisdom": "green", "humour": "yellow", "honour": "cyan"
               }
    styling = str(colours[text])
    return styling


def get_cards():
    """Call to API for full deck of Avatar cards"""
    url = "https://api-generator.retool.com/dqbG1V/airbender"
    response = requests.get(url, timeout=5)
    card_api = response.json()
    deck = []
    for card in card_api:
        avatar_dict = {'name': card['name'], 'bending': card['bending'],
                       'power': card['power'], 'defence': card['defence'],
                       'agility': card['agility'], 'wisdom': card['wisdom'],
                       'humour': card['humour'], 'honour': card['honour']}
        deck.append(avatar_dict)
    return deck


def new_player(name, wins, status):
    """Checks scorecard for player data"""
    user = {'name': [name], 'wins': [wins], 'status': [status]}
    data_frame = pd.DataFrame(user)
    data_frame.to_csv('atla.csv', mode='a', index=False, header=False)
    return user


def user_check(main_player):
    """Checking the Scorecard to see if player exists """
    with open("atla.csv", 'r', encoding='utf-8') as file:
        user_data = csv.DictReader(file)
        player_new = True
        for user in user_data:
            if user['name'] == main_player:
                console.print(f"\nThanks for coming back [bold]{user['name']}[/]. "
                              f"You currently have {user['wins']} wins.")
                player_new = False
                tmp = user
        if player_new:
            wins = 0
            status = True
            tmp = new_player(main_player, wins, status)
            console.print(f"I can see you haven\'t played before [bold]{main_player}[/], "
                          f"Let me explain how this game works:")
            print("The aim of this game is to capture your opponent\'s cards.\n"
                  "By selecting the stats on your cards,"
                  "you can trump the other players stat to capture it.\n"
                  "Once you have captured all of the other player's cards,"
                  "you have won the game.\n"
                  "")
    return tmp


def get_opponent():
    """Establishes opponent name for the player"""
    opponents = ('Joo Dee', 'the Cabbage Merchant', 'Jeong Jeong', 'Gran-Gran',
                 'The Boulder', 'Ty Lee', 'Haru', 'Master Pakku', 'Meelo')
    opponent = random.choice(opponents)
    console.print(f"You will be playing against [bold gold3]{opponent}[/] today.\n")
    return opponent


def shuffle(deck):
    """Shuffles the deck and splits them between player and opponent"""
    # Shuffle The Deck
    shuffled_deck = list(range(len(deck)))
    random.shuffle(shuffled_deck)

    # Turn Deck Into Index Only + Split In Half
    split_deck = len(shuffled_deck) // 2
    deck1_index = shuffled_deck[:split_deck]
    deck2_index = shuffled_deck[split_deck:]

    # Repopulate The Split Decks
    pl_cards = []
    op_cards = []
    for i in deck1_index:
        pl_cards.append(deck[i])
    for i in deck2_index:
        op_cards.append(deck[i])
    print('Let me shuffle the deck and deal the cards to you both.')
    time.sleep(0.5)
    delay = "..................."
    for delays in range(3):
        print(delay, end='')
        time.sleep(0.5)
    count = len(pl_cards)
    console.print(f"\nI have shuffled the deck and split the cards so that you have "
                  f"[bold underline white]{count}[/] each.\n")
    return pl_cards, op_cards


def update_player(name, score, status):
    """Updates the player's wins and player status"""
    data_frame = pd.read_csv('atla.csv')
    data_frame.loc[data_frame['name'] == name, ['wins', 'status']] = [score, status]
    data_frame.to_csv('atla.csv', mode='w', index=False, header=True)


def opponent_pick(cards):
    """Function that chooses a card for the opponent"""
    data_frame = pd.DataFrame(cards, index=[0])
    tmp = data_frame.drop(['name', 'bending'], axis=1)
    answer = random.choice(tmp.keys())
    return answer


def get_rank(name):
    """Gets the rank of the player and checks if tied position"""
    data = pd.read_csv('atla.csv', index_col=0)
    tmp = pd.DataFrame(data)
    # is there a tie ?
    ties = tmp["wins"].duplicated(keep=False)
    # calculate rankings
    ranks = tmp["wins"].rank(method="dense", ascending=False)
    tmp["position"] = (
        ranks.where(~ties, ranks.astype(str).radd("T"))
        .astype(str)
        .replace(".0$", "", regex=True)
    )
    data_frame = tmp.sort_values(by="wins", ascending=False)
    position = (data_frame.at[name, 'position'])
    total = len(data_frame)
    player_position = inflect.engine()
    if position.startswith('T') is True:
        tied_ranking = position.replace('T', '')
        ranking = player_position.ordinal(tied_ranking)
        print(f"You are currently tied {ranking} in the rankings out of {total} users.")

    else:
        ranking = player_position.ordinal(data_frame.at[name, 'position'])
        total = len(data_frame)
        print(f"You are currently ranked {ranking} of {total} users.")


def play_game(pl_cards, op_cards,
              player_won_last, opponent_name):
    """Main gameplay function that compares card stats and outcome"""

    space = str("===================================") * 3
    print(space)
    console.print(f"\nYour card is: [bold]{pl_cards[0]['name']}[/]\n" +
                  "This card\'s stats are:"
                  "   [red]power " + str(pl_cards[0]["power"]) + "[/]" +
                  "   [blue]defence " + str(pl_cards[0]["defence"]) + "[/]" +
                  "   [magenta]agility " + str(pl_cards[0]["agility"]) + "[/]" +
                  "   [green]wisdom " + str(pl_cards[0]["wisdom"]) + "[/]" +
                  "   [yellow]humour " + str(pl_cards[0]["humour"]) + "[/]" +
                  "   [cyan]honour " + str(pl_cards[0]["honour"]) + "[/]")

    if player_won_last:
        print("Please choose a stat to play:")
        answer = input("I choose.. ").lower()
        while answer not in pl_cards[0].keys() or answer == 'name':
            answer = input("Sorry I didn\'t get that. Can you please choose again? ").lower()
    else:
        answer = opponent_pick(op_cards[0])
        style = get_colour(answer)
        console.print(f"It is {opponent_name}\'s turn to choose. "
                      f"{opponent_name} selects [" + style + f"]{answer}[/]")

    time.sleep(2)
    print('')
    style = get_colour(answer)
    console.print(
        f"Your card {pl_cards[0]['name']}\'s [" + style + f"]{answer}[/]"
        f" is [" + style + f"]{pl_cards[0][answer]}[/]. {opponent_name}\'s card "
        f"is {op_cards[0]['name']} and their [" + style + f"]{answer}[/] "
        f"is [" + style + f"]{op_cards[0][answer]}[/]."
    )
    pl_card = pl_cards[0]
    op_card = op_cards[0]
    pl_cards.pop(0)
    op_cards.pop(0)

    if int(pl_card[answer]) > int(op_card[answer]):
        console.print("[bold]" + player_name + " wins this round!")
        pl_cards.append(op_card)
        pl_cards.append(pl_card)
        player_won_last = True
        pl_cards = pl_cards + draw_cards
        draw_cards.clear()
        player_count = str(len(pl_cards))
        opponent_count = str(len(op_cards))
        console.print(
            f"You now have [bold underline white]{player_count}[/] cards and "
            f"{opponent_name} has [bold underline white]{opponent_count}[/] cards.\n")
        time.sleep(2)

    elif int(pl_card[answer]) < int(op_card[answer]):
        console.print("[bold gold3]" + opponent_name + "[/] wins this round!")
        player_won_last = False
        op_cards.append(op_card)
        op_cards.append(pl_card)
        op_cards = op_cards + draw_cards
        draw_cards.clear()
        player_count = str(len(pl_cards))
        opponent_count = str(len(op_cards))
        console.print(
            f"You now have [bold underline white]{player_count}[/] cards and "
            f"{opponent_name} has [bold underline white]{opponent_count}[/] cards.\n")
        time.sleep(2)

    else:
        print(f"{op_card['name']} and {pl_card['name']}\'s {answer} stats are the same!\n")
        draw_cards.append(pl_card)
        draw_cards.append(op_card)
        draw_count = str(len(draw_cards))
        player_count = str(len(pl_cards))
        opponent_count = str(len(op_cards))
        player_won_last = not player_won_last
        console.print(
            f"Your [bold]{pl_card['name']}[/] card and {opponent_name}\'s "
            f"[bold]{op_card['name']}[/] card are placed in the middle.\n"
            f"The winner of the next round will capture these cards.")
        console.print(
            f"You now have [bold underline white]{player_count}[/] cards, "
            f"[bold]{opponent_name}[/] has [bold underline white]{opponent_count}[/] "
            f"cards and there are [underline orange1]{draw_count}[/] cards in the middle.\n")
        if player_won_last is True:
            console.print("[italic]Please choose again..[/]")
        else:
            time.sleep(4)
    return player_won_last, pl_cards, op_cards


def game_outcome(pl_info, opponent_name):
    """Determines who has won the match and if user wants to play again"""
    play_again = "yes"
    player_won_last = True
    full_deck = get_cards()
    while play_again == "yes":
        player_cards, opponent_cards = shuffle(full_deck)
        while len(player_cards) > 0 \
                and len(opponent_cards) > 0:
            player_won_last, player_cards, \
                opponent_cards = play_game(player_cards, opponent_cards,
                                           player_won_last, opponent_name)
            if len(player_cards) == 0:
                if pl_info['status'] is True:
                    pl_info['status'] = False
                    update_player(pl_info['name'], 0, pl_info['status'])
                    print(
                        "Sorry you lost on your first try, "
                        "but please don't be discouraged. "
                        "I'm sure you can win next time. ")
                else:
                    print(
                        f"Sorry you lost today, "
                        f"{opponent_name} is a really strong player. "
                        f"Your score is still {player_info['wins']} wins, "
                        f"but maybe you can win on your next try.")
            if len(opponent_cards) == 0:
                score = int(pl_info['wins']) + 1
                pl_info['status'] = False
                print(f"Congratulations {pl_info['name']}, "
                      f"you won the match!!\n"
                      f"Your score is now at {score} wins.\n")
                update_player(pl_info['name'], score, pl_info['status'])

        play_again = " "
        while play_again != "yes" and play_again != "no":
            play_again = input(f"Would you like to play against "
                               f"{opponent_name} again? [[yes or no]] ").lower()
            if play_again != "yes" and play_again != "no":
                print("Sorry I didn\'t get that. Can you please choose again?")

        if play_again == "no":
            get_rank(pl_info['name'])
            print('Thank you for playing today.')
        else:
            print('Thanks for choosing to play again.')
            get_rank(pl_info['name'])
            player_cards.clear()
            opponent_cards.clear()


# Start Game: player input name to be checked in scorecard
player_name = input(
    "Welcome to Avatar: The Last Airbender Top Trumps. "
    "Please input your name if you'd like to play. ")
player_info = user_check(player_name)
opponent_info = get_opponent()
game_outcome(player_info, opponent_info)
