import skilstak.colors as c
from time import sleep
from random import shuffle

def create_cards():
    suits = ['diamonds', 'clubs', 'hearts', 'spades']
    values = [['ace', 11], ['jack', 10], ['queen', 10], ['king', 10], ['2', 2], ['3', 3], ['4', 4], ['5', 5], ['6', 6], ['7', 7], ['8', 8], ['9', 9], ['10', 10]]
    standard_deck = []
    for card_list in values:
        for suit in suits:
            word = card_list[0] + " of " + suit
            value = card_list[1]
            minilist = [word, value]
            standard_deck.append(minilist)
    return standard_deck


def print_rules():
    print('''{}Objective{}:Get as close to 21 points without going over.
{}How to win{}:Be the closest to 21 points. If you go over, you lose.
{}Point values{}:All cards are worth the value on the card, and face cards are worth 10.
{}Aces{}:Aces can be used as 1 or 11 points.'''.format(c.y, c.x, c.y, c.x, c.y, c.x, c.y, c.x))
    input('Press enter to continue.\n')


def knows_how_to_play():
    answered = False
    while answered is False:
        answer = input('{}{}Does everyone know how to play blackjack?({}Y{}/{}n{}) > {}'.format(c.x, c.cl, c.g, c.x, c.r, c.x, c.c)).lower().strip()
        if 'y' in answer:
            answered = True
        elif 'n' in answer:
            answered = True
            print_rules()
        else:
            print('{}Invalid. Please say {}yes{} or {}no{}.'.format(c.x, c.g, c.x, c.r, c.x))


def is_ace(card):
    if 'ace' in card:
        return True
    return False


def has_ace(aces):
    has_ace = False
    for ace in aces:
        if ace == 11:
            aces.remove(11)
            aces.append(1)
            has_ace = True
            break
    return has_ace, aces


def get_two_cards(deck):
    card = deck.pop()
    card2 = deck.pop()
    if is_ace(card[0]) and is_ace(card2[0]):
        total = 12
    else:
        total = card[1] + card2[1]
    title_one = card[0]
    title_two = card2[0]
    return title_one, title_two, total, deck


def get_players():
    try:
        while True:
            players = input('How many players? > ' + c.c)
            if players.isdigit():
                return int(players)
            else:
                print('{}Please type a {}number{}.'.format(c.x, c.r, c.x))
    except KeyboardInterrupt:
        print(c.cl)
        exit()


def print_hand(title_one, title_two, total):
    print('Your hand contains the {}{}{} and the {}{}{} for a total of {}{}{} points.'.format(c.b, title_one, c.x, c.b, title_two, c.x, c.m, total, c.x))


def get_one_more_card(deck, total):
    card = deck.pop()
    title = card[0]
    total += card[1]
    print('{}Your new card is the {}{}{}. You now have {}{}{} Points.'.format(c.x, c.b, title, c.x, c.m, total, c.x))
    return total, deck, title


def ask_to_hit(hand, first_time):
    try:
        while True:
            item_string = 'Your hand contains:'
            for item in hand:
                item_string += item + ' '
            if first_time is False:
                print(item_string)
            want_to_hit = input('Would you like to hit (take another card)? (y/n) > ' + c.c).strip().lower()
            if 'y' in want_to_hit:
                return True
                break
            elif 'n' in want_to_hit:
                return False
                break
            else:
                print('{}Please type {}yes{} or {}no{}.'.format(c.x, c.g, c.x, c.r, c.x))
    except KeyboardInterrupt:
        print(c.cl)
        exit()


def get_round_values(players):
    first_time = []
    hands = []
    totals = []
    aces = []
    for x in range(players):
        first_time.append(True)
        totals.append(0)
        hands.append([])
        aces.append([])
    return first_time, hands, totals, aces


def gen_perm_values(num_of_players):
    ties = []
    wins = []
    losses = []
    names = []
    for x in range(num_of_players):
        ties.append(0)
        wins.append(0)
        losses.append(0)
        names.append('Player ' + str(x))
    return names, wins, ties, losses 


def find_best(totals, hands):
    highest = 0
    shortest = 999
    for total in totals:
        if total < 22:
            if total > highest:
                highest = total
    for x in range(len(totals)):
        if totals[x] == highest and len(hands[x]) < shortest:
            shortest = len(hands[x])

    return highest, shortest


def find_winners(totals, hands, losses):
    highest, shortest = find_best(totals, hands)
    winners = []
    for x in range(len(totals)):
        if totals[x] == highest and len(hands[x]) == shortest:
            winners.append(x)
        else:
            losses[x] += 1
    return winners, losses


def add_aces(card1, card2, aces):
    if is_ace(card1):
        aces.append(11)
    elif is_ace(card2):
        aces.append(11)
    return aces


def print_winners(player_names, winners, wins, ties):
    if len(winners) > 1:
        names = ''
        string = 'The winners are:'
        for name in winners:
            ties[name] += 1
            names += player_names[name] + ' '
        print(string + c.o+names+c.x)
    elif len(winners) == 1:
        print('{}The winner is {}{}{}!'.format(c.x, c.g, player_names[winners[0]], c.x))
        wins[winners[0]] += 1
    else:
        print('{}Nobody{} won this round!'.format(c.r, c.x))
    return wins, ties


def print_data(player_names, wins, ties, losses, stage, hands, totals):
    for i in range(len(player_names)):
        hand = ""
        for card in hands[i]:
            hand += (card + ", ")
        hand = hand[:-2]
        print("{}{}{}'s card's include: {}{}{} for a total of: {}{}{} points.".format(c.m, player_names[i], c.x, c.y, hand, c.x, c.b, totals[i], c.x))
    print('\nplayer  |wins|ties|losses|%win/tie|%lose')
    for x in range(len(player_names)):
        losspercent = round(losses[x]/(stage+1)*100, 2)
        winpercent = 100 - losspercent
        print('{}|{}   |{}   |{}     |{}    |{}    '.format(player_names[x], wins[x], ties[x], losses[x], winpercent, losspercent))
    print('\n\n')


def print_intro():
    print('''{}{}Welcome to {}Blackjack{}!
Created by: {}Peter S.{}
Version: {}0.9.9{}'''.format(c.x, c.cl, c.g, c.x, c.b, c.x, c.m, c.x))


def print_starting_data(rounds):
    print('''{}{}Maximum rounds: {}{}{}
Decks used: {}8{}
{}Note{}: Earlier players are at a disadvantage
if you let other people look at your screen.'''.format(c.cl, c.x, c.y, rounds-1, c.x, c.y, c.x, c.y, c.x))


def pass_to_next(players, z):
    if z != players-1:
        print('{}{}Pass to Next Player within 5 seconds{}'.format(c.cl, c.r, c.x))
        sleep(5)
    print(c.cl)
def handle_betting(players, hands, first_time, z, deck, totals, aces):
    while True:
        wants_to_hit = ask_to_hit(hands[z], first_time)
        if wants_to_hit is True:
            first_time[z] = False
            totals[z], deck, title = get_one_more_card(deck, totals[z])
            if 'ace' in title:
                aces[z].append(11)
            hands[z].append(title)
            if totals[z] > 21:
                has_an_ace, aces[z] = has_ace(aces[z])
                if has_an_ace is False:
                    print('Oh No! You busted.')
                    sleep(3)
                    pass_to_next(players, z)
                    break
                else:
                    totals[z] -= 10
                    print(c.x + 'You went over, so your ace valued 11 was changed into a 1.')
                    print('You now have {}{}{} points.'.format(c.b, totals[z], c.x))

        else:
            pass_to_next(players, z)
            break
    return totals, deck


def start_game():
    print_intro()
    players = get_players()
    deck = create_cards() * 8
    rounds = round((52 * 8) / (4 * players))
    shuffle(deck)
    player_names, wins, ties, losses = gen_perm_values(players)
    print_starting_data(rounds)
    return players, player_names, wins, ties, losses, deck, rounds


