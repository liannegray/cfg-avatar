import random
import pandas as pd
import csv

# Global variables for card deck, player and opponent cards
full_deck = []
draw_cards = []
player_cards = []
opponent_cards = []
player_won_last = False
opponent_won_last = False


def cards(name, bending, power, defence, agility, wisdom, humour, honour):
    avatar_dict = {'name': name, 'bending': bending, 'power': power,
                   'defence': defence, 'agility': agility, 'wisdom': wisdom,
                   'humour': humour, 'honour': honour}
    full_deck.append(avatar_dict)


# playing cards deck --- make into API??
cards('Aang', 'Air', 10, 10, 10, 10, 6, 10)
cards('Katara', 'Water', 9, 8, 6, 9, 2, 5)
cards('Sokka', 'None', 5, 2, 4, 7, 10, 7)
cards('Toph', 'Earth', 10, 10, 7, 1, 9, 1)
cards('Zuko', 'Fire', 9, 3, 9, 8, 2, 9)
cards('Iroh', 'Fire', 10, 9, 5, 10, 8, 5)
cards('Suki', 'None', 7, 7, 8, 6, 3, 8)
cards('Bumi', 'Earth', 9, 9, 7, 5, 5, 0)
cards('Admiral Zhao', 'Fire', 8, 4, 3, 9, 1, 5)
cards('Azula', 'Fire', 10, 1, 8, 0, 0, 2)


def new_player(name, wins, status):
    user = {'name': [name], 'wins': [wins], 'status': [status]}
    df = pd.DataFrame(user)
    df.to_csv('atla.csv', mode='a', index=False, header=False)
    return user


def user_check(player_name):
    with open("atla.csv", 'r') as file:
        user_data = csv.DictReader(file)
        player_new = True

        for user in user_data:
            if user['name'] == player_name:
                print(f"Thanks for coming back {user['name']}. "
                      f"You currently have {user['wins']} wins.\n")
                player_new = False
                tmp = user

        if player_new:
            wins = 0
            status = True
            tmp = new_player(player_name, wins, status)
            print(f"I can see you haven\'t played before {player_name}, Let me explain how this game works:")
            print(f"The aim of this game is to capture your opponent\'s cards. "
                  f"By selecting the stats on your cards, you can trump the other players stat to capture it.")
            print(f"Once you have captured all of the other player's cards, you have won the game.\n")
    return tmp


def get_opponent():
    opponents = ('Joo Dee', 'Cabbage Merchant', 'Jeong Jeong', 'Gran-Gran',
                 'The Boulder', 'Ty Lee', 'Haru')
    opponent = random.choice(opponents)
    print(f"You will be playing against {opponent} today.")
    return opponent


def shuffle(full_deck):
    # Shuffle The Deck
    shuffled_deck = list(range(len(full_deck)))
    random.shuffle(shuffled_deck)

    # Turn Deck Into Index Only + Split In Half
    split_deck = len(shuffled_deck) // 2
    deck1_index = shuffled_deck[:split_deck]
    deck2_index = shuffled_deck[split_deck:]

    # Repopulate The Split Decks
    for i in deck1_index:
        player_cards.append(full_deck[i])
    for i in deck2_index:
        opponent_cards.append(full_deck[i])
    print('Let me shuffle the deck and deal the cards to you both.')
    print('...')
    print('...')


def update_player(name, score, status):
    df = pd.read_csv('atla.csv')
    df.loc[df['name'] == name, ['wins', 'status']] = [score, status]
    df.to_csv('atla.csv', mode='w', index=False, header=True)


# Start Game
player_name = input("Welcome to Avatar: The Last Airbender Top Trumps. Please input your name if you'd like to play. ")
player_info = user_check(player_name)
opponent_name = get_opponent()
shuffle(full_deck)
print('I have shuffled the deck and split the cards so that you have 5 each.')
while len(player_cards) > 0 and len(opponent_cards) > 0:
    print('Your card is: {}.'.format(player_cards[0]['name']) + ' This card\'s stats are: power ' + str(
        player_cards[0]["power"]) + '   defence ' + str(player_cards[0]["defence"]) + '   agility ' + str(
        player_cards[0]["agility"]) + '   wisdom ' + str(player_cards[0]["wisdom"]) + '   humour ' + str(
        player_cards[0]["humour"]) + '   honour ' + str(player_cards[0]["honour"]))
    print(f"Please choose a stat to play {player_name}")

    answer = input('I choose.. ').lower()
    while answer not in player_cards[0].keys() or answer == 'name':
        answer = input('Sorry I didn\'t get that. Can you please choose again.').lower()
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
        print('You have {} cards and {} has {} cards.'.format(str(len(player_cards)), opponent_name,
                                                              str(len(opponent_cards))))

    elif pc[answer] < oc[answer]:
        print(opponent_name + ' wins this round!')
        opponent_cards.append(oc)
        opponent_cards.append(pc)
        player_won_last = False
        opponent_won_last = True
        opponent_cards = opponent_cards + draw_cards
        draw_cards.clear()
        print('You have {} cards and {} has {} cards.'.format(str(len(player_cards)), opponent_name,
                                                              str(len(opponent_cards))))

    else:
        print("It's a tie, please choose again.")
        draw_cards.append(pc)
        draw_cards.append(oc)
if len(player_cards) == 0:
    if player_info['status'] is True:
        print(f"Sorry you lost on your first try, but please don't be discouraged."
              f"Your score is {player_info['wins']} wins, but I'm sure you can win if you try again. ")
    else:
        print(f"Sorry you lost today, {opponent_name} is a really strong player. "
              f"Your score is still {player_info['wins']} wins, but maybe you can win on your next try.")

else:
    score = int(player_info['wins']) + 1
    print(f"Congratulations {player_info['name']}, you won the match! "
          f"Your score is now at {score} wins.")
    update_player(player_info['name'], score, player_info['status'])
