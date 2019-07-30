import random
import sys

suit_types = ('Diamond', 'Heart', 'Spades', 'Clubs')
ranks_types = ('Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'King', 'Queen')
card_values = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'King': 10, 'Queen': 10
               , 'Jack': 10, '11': 11}


# THE FOR LOOP IN THE CLASS WILL GENERATE ALL 52 COMBINATIONS OF suits and ranks.
class Deck:
    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks
        self.deck = []

        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append('{} of {}'.format(rank, suit))

    # THIS METHOD IS NOT NEEDED FOR THE GAME, IT SHOWS THE CARDS IN THE DECK.
    def deck_of_cards(self):
        return self.deck

    # RETURNS THE LENGTH OF THE DECK (52)
    def length(self):
        return len(self.deck)

    # SHUFFLES THE DECK
    def shuffle(self):
        random.shuffle(self.deck)
        return self.deck

    # PICKS A RANDOM CARD WHEN PLAYER WANTS A HIT.
    def hit(self):
        return random.choice(self.deck)

    # DEALS TWO CARDS FOR THE PLAYER AND THE DEALER
    def deal(self):
        return [random.choice(self.deck), random.choice(self.deck)]


# THIS CLASS TAKES CARE OF THE CHIPS (ACCOUNT)
class PlayerAccount:

    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.player_bet = 0

    # ACCEPTS A BET FROM THE PLAYER AND CHECKS IF BETS ARE USABLE.
    def bet(self):
        # Get the player's bet and store it in the class variable.
        self.player_bet = int(input('How much do you wish to bet? '))

        if self.player_bet > self.chips:
            print('Not enough chips dude!!!')
            player_ans = input('\nDo you want to add more chips, reduce your bet, or quit (add, reduce, quit)? ')

            while True:
                # If player chose to add.
                if player_ans == 'Add' or player_ans == 'add':
                    add_amount = int(input('Enter amount to add: '))

                    # Check if added amount is enough.
                    while True:
                        self.chips = self.chips + add_amount
                        if self.player_bet < self.chips:
                            print('Added amount accepted. You have a total of {} chips.'.format(self.chips))
                            return 'You now have {} chips remaining after betting.'.format(self.chips - self.player_bet)
                        else:
                            print('Your balance is still low!!!\n')
                        add_amount = int(input('Enter amount to add: '))

                # If player chose to reduce bet.
                elif player_ans == 'Reduce' or player_ans == 'reduce':
                    self.player_bet = int(input('Enter new bet: '))

                    # Check if new bet is acceptable.
                    while True:
                        if self.player_bet <= self.chips:
                            return 'New bet accepted.\n' \
                                   'You now have {} chips remaining after betting.'.format(self.chips - self.player_bet)
                        else:
                            print('Your bet is still high man.\n')
                        self.player_bet = int(input('Enter new bet: '))

                # If player chose to quit.
                elif player_ans == 'Quit' or player_ans == 'quit':
                    sys.exit()

                else:
                    player_ans = input('\nEnter one of the options (add, reduce, quit)? ')

        else:
            balance = self.chips - self.player_bet
            return 'Bet accepted. You have {} chips remaining after betting.'.format(balance)

    # ALLOWS PLAYER TO ADD MORE CHIPS TO THE ACCOUNT.
    def winning_chips(self):
        self.chips = self.chips + self.player_bet
        return self.chips

    # CALCULATES THE NUMBER OF CHIPS REMAINING
    def losing_chips(self):
        self.chips = self.chips - self.player_bet
        return self.chips

    def remaining_chips(self):
        return self.chips


# THIS FUNCTION WILL TELL US THE VALUE OF THE CARD
def value(card, player_type):
    if card == 'Ace' and player_type == 'player':
        user_ans = int(input('\nDo you want to use your Ace as a 1 or 11? '))
        if user_ans == 1:
            return '1'
        elif user_ans == 11:
            return '11'
    elif card == 'Ace' and player_type == 'dealer':
        return random.choice(['1', '11'])
    else:
        return card


# CREATE PLAYER PROFILE, A DECK OF CARDS AND PLAYER ACCOUNT FOR THE CHIPS
player_name = input('What is your name? ')
player_chips = int(input("How many chips do you want to deposit? "))
game_deck = Deck(suit_types, ranks_types)
player = PlayerAccount(player_name, player_chips)


# THIS FUNCTION WILL DEAL CARDS TO THE USER AND DEALER, AND CALCULATE THEIR VALUES.
def master_dealer():
    global player_cards
    global player_value
    global dealer_cards
    global dealer_value

    # Deal cards to player and dealer
    player_cards = game_deck.deal()
    dealer_cards = game_deck.deal()

    # SHOW AND CALCULATE THE VALUE OF THE PLAYER'S CARDS
    print('\nHere are your cards:')
    print('\n'.join(player_cards))
    player_value = card_values[value(player_cards[0].split()[0], 'player')] + card_values[value(player_cards[1].
                                                                                                split()[0], 'player')]

    # IF THE PLAYER HAS AN ACE AND CHOSE TO USE IT AS AN 11, THEN PLAYER MIGHT WIN IF HER OTHER CARD IS A 10
    if player_value == 21:
        print('You win!!!!!!!!!!!!!!! \n'
              'You now have {} chips.'.format(player.winning_chips()))

        # CALL FUNCTION TO ASK IF TO PLAY AGAIN.
        if game_replay() == 'yes':
            game_play()
        elif game_replay() == 'no':
            sys.exit()

    # SHOW AND CALCULATE ONE OF THE DEALER'S CARDS.
    print('\nHere is one of the dealers cards: ')
    print(random.choice(dealer_cards))
    dealer_value = card_values[value(dealer_cards[0].split()[0], 'dealer')] + card_values[value(dealer_cards[1].
                                                                                                split()[0], 'dealer')]


# THE HIT OR STAY FUNCTION.
def hit_stay():
    global player_value
    global dealer_value
    stay_check = False

    # ASK THE PLAYER TO HIT OR STAY.
    player_choice = input('\nDo you wish to hit or stay (hit or stay)? ')

    while True:
        if player_choice == 'Hit' or player_choice == 'hit':
            player_hit_card = game_deck.hit()
            print(player_hit_card)

            # ADD THE VALUE OF THE HIT CARD TO THE SUM OF THE PLAYER'S CARDS
            player_hit_value = card_values[value(player_hit_card.split()[0], 'player')]
            player_value = player_value + player_hit_value

            if player_value > 21:
                print('Bust!!!!!!!!!!!!!!!!!!!! \n'
                      'Dealer wins! You have {} chips left.\n'.format(player.losing_chips()))
                break

            elif player_value == 21:
                print('You win!!!!!!!!!!!!!!! \n'
                      'You now have {} chips.\n'.format(player.winning_chips()))
                break

        elif player_choice == 'stay' or player_choice == 'Stay':
            stay_check = True
            break

        else:
            player_choice = input('\nYoo, enter one of these options (hit or stay)? ')
            continue

        # ASK THE PLAYER TO HIT OF STAY TO MAINTAIN THE LOOP.
        player_choice = input('\nDo you wish to hit or stay (hit or stay)? ')

    # IF PLAYER STAYS, DEALER WILL HAVE TO HIT UNTIL HE EITHER WINS OR LOSES.
    while stay_check:
        dealer_hit_card = game_deck.hit()
        print(dealer_hit_card)

        # ADD THE VALUE OF THE HIT CARD TO THE SUM OF THE DEALER'S CARDS
        dealer_value = dealer_value + card_values[value(dealer_hit_card.split()[0], 'dealer')]
        # print(dealer_value)

        # CHECK IF THE DEALER BUSTS
        if player_value < dealer_value <= 21:
            print('Dealer wins! You have {} chips left.'.format(player.losing_chips()))
            break

        elif dealer_value > 21:
            print('Dealer bust!!!!!\n'
                  'You win!!!!!!!!!\n'
                  'You now have {} chips.\n'.format(player.winning_chips()))
            break
        else:
            continue


# CHECK IF THERE ARE ENOUGH CHIPS TO REPLAY THE GAME.
def chip_checker():
    global player_chips
    global player

    if player.remaining_chips() <= 0:
        print("Bruh, you're broke!!!\n")
        player_response = input('Do you want to add more chips or quit the game (add or quit)? ')

        if player_response == 'Add' or player_response == 'add':
            player_chips = int(input('How many chips do you want to add? '))
            player = PlayerAccount(player_name, player_chips)
            return player_chips

        elif player_response == 'Quit' or player_response == 'quit':
            sys.exit()

    else:
        return player.remaining_chips()


# THE REPLAY FUNCTION
def game_replay():
    # RESET THE PLAYER AND DEALER VALUES
    global player_value
    global dealer_value

    replay = input('Do you want to play again (yes or no)? ')
    while True:
        if replay == 'Yes' or replay == 'yes':
            player_value = 0
            dealer_value = 0
            return 'yes'
        elif replay == 'No' or replay == 'no':
            return 'no'
        else:
            replay = input("C'mon, enter either yes or no, mate: ")


# PLAY THE GAME
def game_play():
    while True:
        # TAKE A BET AND SHUFFLE THE DECK
        print(player.bet())
        game_deck.shuffle()

        # INVOKE THE MASTER DEALER
        master_dealer()

        # HIT OR STAY (PLAY THE GAME)
        print(hit_stay())

        # CHECK IF THERE ARE ENOUGH CHIPS AND ASK IF THE USER WANTS TO PLAY AGAIN
        play_again = game_replay()
        if play_again == 'yes':
            chip_checker()
        elif play_again == 'no':
            sys.exit()


# GLOBAL VARIABLES.
player_cards = 'card'
player_value = 0
dealer_cards = 'cards'
dealer_value = 0

game_play()



