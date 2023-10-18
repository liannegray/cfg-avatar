import random
import time
import csv
import inflect
import pandas as pd
import requests

# Global variables for card deck, player and opponent cards
all_cards = []
draw_cards = []
player_cards = []
opponent_cards = []
player_won_last = True
opponent_won_last = False


def get_cards(deck):
    url = 'https://retoolapi.dev/xSDZHt/airbender'
    response = requests.get(url)
    card_api = response.json()
    for card in card_api:
        avatar_dict = {'name': card['name'], 'bending': card['bending'], 'power': card['power'],
                       'defence': card['defence'], 'agility': card['agility'], 'wisdom': card['wisdom'],
                       'humour': card['humour'], 'honour': card['honour']}
        deck.append(avatar_dict)
    return deck


def new_player(name, wins, status):
    user = {'name': [name], 'wins': [wins], 'status': [status]}
    df = pd.DataFrame(user)
    df.to_csv('atla.csv', mode='a', index=False, header=False)
    return user


def user_check(player):
    with open("atla.csv", 'r') as file:
        user_data = csv.DictReader(file)
        player_new = True

        for user in user_data:
            if user['name'] == player:
                print(f"Thanks for coming back {user['name']}. "
                      f"You currently have {user['wins']} wins.\n")
                player_new = False
                tmp = user

        if player_new:
            wins = 0
            status = True
            tmp = new_player(player, wins, status)
            print(f"I can see you haven\'t played before {player}, "
                  f"Let me explain how this game works:")
            print(
                f"The aim of this game is to capture your opponent\'s cards. "
                f"By selecting the stats on your cards, "
                f"you can trump the other players stat to capture it.")
            print(f"Once you have captured all of the other player's cards, "
                  f"you have won the game.\n")
    return tmp


def get_opponent():
    opponents = ('Joo Dee', 'the Cabbage Merchant', 'Jeong Jeong', 'Gran-Gran',
                 'The Boulder', 'Ty Lee', 'Haru')
    opponent = random.choice(opponents)
    print(f"You will be playing against {opponent} today.")
    return opponent


def shuffle(deck):
    # Shuffle The Deck
    shuffled_deck = list(range(len(deck)))
    random.shuffle(shuffled_deck)

    # Turn Deck Into Index Only + Split In Half
    split_deck = len(shuffled_deck) // 2
    deck1_index = shuffled_deck[:split_deck]
    deck2_index = shuffled_deck[split_deck:]

    # Repopulate The Split Decks
    for i in deck1_index:
        player_cards.append(deck[i])
    for i in deck2_index:
        opponent_cards.append(deck[i])
    print('Let me shuffle the deck and deal the cards to you both.')
    time.sleep(1)
    delay = "..................."
    for x in range(3):
        print(delay, end='')
        time.sleep(1)
    print('')
    print('I have shuffled the deck and split the cards so that you have 5 each.\n')


def update_player(name, wins, status):
    df = pd.read_csv('atla.csv')
    df.loc[df['name'] == name, ['wins', 'status']] = [wins, status]
    df.to_csv('atla.csv', mode='w', index=False, header=True)


def opponent_pick(cards):
    df = pd.DataFrame(cards, index=[0])
    tmp = df.drop(['name', 'bending'], axis=1)
    pick = random.choice(tmp.keys())
    return pick


def get_rank(name):
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
    df = tmp.sort_values(by="wins", ascending=False)
    position = (df.at[name, 'position'])
    total = len(df)
    p = inflect.engine()
    if position.startswith('T') is True:

        tied_ranking = position.replace('T', '')
        ranking = p.ordinal(tied_ranking)
        print(f"You are currently tied {ranking} in the rankings out of {total} users.")

    else:
        ranking = p.ordinal(df.at['Lianne', 'position'])
        total = len(df)
        print(f"You are currently ranked {ranking} of {total} users.")


# Start Game
player_name = input(
    "Welcome to Avatar: The Last Airbender Top Trumps. "
    "Please input your name if you'd like to play. ")
player_info = user_check(player_name)
opponent_name = get_opponent()
full_deck = get_cards(all_cards)

while True:
    shuffle(full_deck)
    while len(player_cards) > 0 and len(opponent_cards) > 0:
        print('Your card is: {}. '.format(player_cards[0]['name']) +
              'This card\'s stats are:'
              '   power ' + str(player_cards[0]["power"]) +
              '   defence ' + str(player_cards[0]["defence"]) +
              '   agility ' + str(player_cards[0]["agility"]) +
              '   wisdom ' + str(player_cards[0]["wisdom"]) +
              '   humour ' + str(player_cards[0]["humour"]) +
              '   honour ' + str(player_cards[0]["honour"]))

        if player_won_last:
            print(f"Please choose a stat to play:")
            answer = input("I choose.. ").lower()
            while answer not in player_cards[0].keys() or answer == 'name':
                answer = input('Sorry I didn\'t get that. Can you please choose again?').lower()
        else:
            answer = opponent_pick(opponent_cards[0])
            print(f"It is {opponent_name}\'s turn to choose. "
                  f"{opponent_name} selects {answer}")

        time.sleep(2)
        print('')
        print('Your card {}\'s {} is {}. {}\'s card is {} and their {} is {}.'.format(
            player_cards[0]['name'], answer, player_cards[0][answer],
            opponent_name, opponent_cards[0]['name'], answer, opponent_cards[0][answer]))

        pc = player_cards[0]
        oc = opponent_cards[0]
        player_cards.pop(0)
        opponent_cards.pop(0)

        if pc[answer] > oc[answer]:
            print(player_name + ' wins this round!')
            player_cards.append(oc)
            player_cards.append(pc)
            player_won_last = True
            opponent_won_last = False
            player_cards = player_cards + draw_cards
            draw_cards.clear()
            player_count = str(len(player_cards))
            opponent_count = str(len(opponent_cards))
            print(
                f"You now have {player_count} cards and {opponent_name} has {opponent_count} cards.\n")
            time.sleep(2)

        elif pc[answer] < oc[answer]:
            print(opponent_name + ' wins this round!')
            opponent_cards.append(oc)
            opponent_cards.append(pc)
            player_won_last = False
            opponent_won_last = True
            opponent_cards = opponent_cards + draw_cards
            draw_cards.clear()
            answer = None
            player_count = str(len(player_cards))
            opponent_count = str(len(opponent_cards))
            print(
                f"You now have {player_count} cards and {opponent_name} has {opponent_count} cards.\n")
            time.sleep(2)

        else:
            print(f"{oc['name']} and {pc['name']}\'s {answer} stats are the same!\n")
            draw_cards.append(pc)
            draw_cards.append(oc)
            draw_count = str(len(draw_cards))
            player_count = str(len(player_cards))
            opponent_count = str(len(opponent_cards))
            print(
                f"Your {pc['name']} card and {opponent_name}\'s {oc['name']} card "
                f"are placed in the middle. The winner of the next round will capture these cards.")
            print(
                f"You now have {player_count} cards, {opponent_name} has {opponent_count} cards and "
                f"there are {draw_count} cards in the middle.\n")
            if player_won_last is True:
                print('Please choose again.')
            else:
                time.sleep(4)

    if len(player_cards) == 0:
        if player_info['status'] is True:
            print(
                f"Sorry you lost on your first try, but please don't be discouraged."
                f"Your score is {player_info['wins']} wins, but I'm sure you can win next time. ")
        else:
            print(
                f"Sorry you lost today, {opponent_name} is a really strong player. "
                f"Your score is still {player_info['wins']} wins, but maybe you can win on your next try.")

    else:
        score = int(player_info['wins']) + 1
        print(f"Congratulations {player_info['name']}, you won the match!\n"
              f"Your score is now at {score} wins.\n")
        update_player(player_info['name'], score, player_info['status'])

    while True:
        play_again = input(f"Would you like to play against {opponent_name} again? [[yes or no]] ").lower()
        if play_again != "yes" or play_again != "no":
            print("Sorry I didn\'t get that. Can you please choose again?")
            continue
        else:
            break
        if play_again == "yes":
            print('Thanks for choosing to play again.')
            get_rank(player_info['name'])
            player_cards.clear()
            opponent_cards.clear()
            continue
        if play_again == "no":
            get_rank(player_info['name'])
            print('Thank you for playing today.')
            break
